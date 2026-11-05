"""Open the archive A321 mesh and its gear animation as an editable Blender file.

D:\\blender.exe --background --factory-startup --python tools/build_a321_gear_blender.py
The site JSON is the source of truth; re-run after tools/add_a321_gear.py.
"""
import bpy
import json
import math
import os
from array import array
from base64 import b64decode
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree


ROOT = Path(__file__).resolve().parents[1]
MODEL = json.loads((ROOT / "models/a321.json").read_text(encoding="utf-8"))
DEST = ROOT / "models/blender/a321_gear.blend"
MATERIALS = {}
GEAR_OBJECTS = []


def blender_vec(v):
    return (v[0], -v[2], v[1])  # Archive Y-up, Blender Z-up.


def material(color):
    key = tuple(color)
    if key not in MATERIALS:
        mat = bpy.data.materials.new("RGBA " + ",".join(f"{x:.2f}" for x in key))
        mat.diffuse_color = (*key[:3], key[3])
        mat.use_nodes = True
        mat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = mat.diffuse_color
        MATERIALS[key] = mat
    return MATERIALS[key]


def make_mesh(name, entry, part, parent=None):
    q = array("H")
    q.frombytes(b64decode(entry["q"]))
    verts = [blender_vec([q[i+k]*entry["qs"][k]+entry["qo"][k] for k in range(3)])
             for i in range(0,len(q),3)]
    indices = array("I" if entry.get("iw") == 4 else "H")
    indices.frombytes(b64decode(entry["i"]))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], [indices[i:i+3] for i in range(0,len(indices),3)])
    mesh.update()
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material(entry["c"]))
    ob["partId"] = part
    if parent:
        bpy.context.view_layer.update()
        ob.parent = parent
        ob.matrix_parent_inverse = parent.matrix_world.inverted()
    return ob


def build():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    shell = None
    for part, entries in MODEL["parts"].items():
        for i, entry in enumerate(entries):
            ob = make_mesh(f"{part}_{i}", entry, part)
            if part == "fuselage" and entry["c"] == [1,1,1,1]:
                shell = ob
    assert shell is not None

    for i, surface in enumerate(MODEL["surfaces"]):
        if surface.get("channel") != "gear":
            for j, entry in enumerate(surface["e"]):
                make_mesh(f"control_surface_{i}_{j}", entry, surface.get("part","wing"))
            continue
        pivot = bpy.data.objects.new(surface["id"], None)
        bpy.context.collection.objects.link(pivot)
        pivot.location = blender_vec(surface["pv"])
        pivot.empty_display_type = "ARROWS"
        pivot.empty_display_size = .25
        pivot["channel"] = "gear"
        pivot.rotation_mode = "AXIS_ANGLE"
        axis = blender_vec(surface["ax"])
        pivot.rotation_axis_angle = (0,*axis)
        pivot.keyframe_insert(data_path="rotation_axis_angle", frame=1)
        pivot.rotation_axis_angle = (surface["angle"],*axis)
        pivot.keyframe_insert(data_path="rotation_axis_angle", frame=61)
        pivot.rotation_axis_angle = (0,*axis)  # Parent children in the deployed pose.
        for j, entry in enumerate(surface["e"]):
            ob = make_mesh(f"{surface['id']}_{j}", entry, "gear", pivot)
            if surface["id"] == "skygear_nose":
                GEAR_OBJECTS.append(ob)

    scene = bpy.context.scene
    scene.frame_end = 61
    scene.unit_settings.system = "METRIC"
    scene.frame_set(61)
    bpy.context.view_layer.update()
    bvh = BVHTree.FromObject(shell, bpy.context.evaluated_depsgraph_get())
    checked = 0
    exposed = 0
    worst = 0.0
    worst_at = None
    lowest = float("inf")
    for ob in GEAR_OBJECTS:
        for vertex in ob.data.vertices:
            p = ob.matrix_world @ vertex.co
            lowest = min(lowest, p.z)
            # Cast from inside the fuselage toward its underside. The original
            # wheel bay is open, so a ray from below may hit the *roof* instead.
            hit, _, _, _ = bvh.ray_cast(Vector((p.x,p.y,1.25)), Vector((0,0,-1)), 2.5)
            if hit:
                checked += 1
                excess = hit.z-p.z
                if excess > .012:
                    exposed += 1
                    if excess > worst:
                        worst, worst_at = excess, (ob.name,tuple(round(v,3) for v in p),tuple(round(v,3) for v in hit))
    print(f"A321 nose gear: lowest={lowest:.4f}; {checked} vertices checked against underside, {exposed} exposed; worst={worst:.4f}; sample={worst_at}")
    assert lowest > .82, "Retracted nose gear drops below the wheel-bay clearance"
    assert checked > 100, "Insufficient fuselage-shell coverage for a meaningful check"
    assert exposed == 0, "Nose gear still protrudes below the fuselage"

    scene.frame_set(1)  # Save the editable file with gear down.
    bpy.context.preferences.filepaths.save_version = 0
    DEST.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(DEST))
    print(f"Saved {DEST}")


if __name__ == "__main__":
    build()
