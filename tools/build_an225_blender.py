"""Build the portable, textured An-225 from its archive rig (run in Blender background mode)."""
import json
import math
from array import array
from base64 import b64decode
from pathlib import Path
import sys

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"tools"))
from export_blender_glb import export

model = json.loads((ROOT/"models/an225.json").read_text(encoding="utf8"))
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.frame_end = 181
scene.render.fps = 30
image = bpy.data.images.load(str(ROOT/model["texture"]))
image.pack()
materials = {}
pivots = {}
centers = {}


def vector(v):
    return Vector((v[0], -v[2], v[1]))


def metres(v):
    return 7*vector(v)


def unpack(entry, key, code):
    result = array(code)
    result.frombytes(b64decode(entry[key]))
    return result


def material(entry):
    key = (entry["t"], tuple(entry["c"]),entry.get("alphaTest"))
    if key in materials:
        return materials[key]
    mat = bpy.data.materials.new("Livery" if key[0] else "Cargo equipment")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = entry["c"]
    if key[0]:
        tex = nodes.new("ShaderNodeTexImage")
        tex.image = image
        mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
        if key[2]:
            mat.node_tree.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    materials[key] = mat
    return mat


def travel(s,t):
    curve = s.get("motion")
    if not curve:
        return t
    for (a,y),(b,z) in zip(curve,curve[1:]):
        if t<=b:
            return y+(z-y)*max(0,(t-a)/(b-a))
    return curve[-1][1]


def amount(channel, frame):
    # First deploy/retract flying controls, then illustrate loading on the ground.
    if channel in ("steer","reverse","wheels"): return max(0,min(1,(frame-81)/4,(91-frame)/5))
    if channel=="loading": return max(0,min(1,(frame-91)/55,(181-frame)/25))
    return max(0,min(1,(frame-1)/40,(81-frame)/30))


def mesh(entry, pid, hinge=None, spec=None):
    name = entry["name"]
    q = unpack(entry,"q","H")
    verts = [metres([q[i+j]*entry["qs"][j]+entry["qo"][j] for j in range(3)])
             for i in range(0,len(q),3)]
    indices = unpack(entry,"i","H" if entry["iw"]==2 else "I")
    geom = bpy.data.meshes.new(name)
    geom.from_pydata(verts,[],[indices[i:i+3] for i in range(0,len(indices),3)])
    geom.update()
    if entry.get("u"):
        uv = unpack(entry,"u","H")
        layer = geom.uv_layers.new()
        layer.data.foreach_set("uv",[value for loop in geom.loops for value in
                                   (uv[2*loop.vertex_index]/65535,1-uv[2*loop.vertex_index+1]/65535)])
    obj = bpy.data.objects.new(name,geom)
    scene.collection.objects.link(obj)
    obj["partId"] = pid
    geom.materials.append(material(entry))
    if hinge is not None:
        obj.parent = hinge
        base = -metres(spec["pv"])
        obj.location = base
        if entry.get("slide"):
            start,end = entry.get("slideStart",0),entry.get("slideEnd",1)
            for frame in range(1,182):
                amt = amount(spec["channel"],frame)
                obj.location = base+metres(entry["slide"])*max(0,min(1,(amt-start)/(end-start)))
                obj.keyframe_insert(data_path="location",frame=frame)


for pid,entries in model["parts"].items():
    for entry in entries: mesh(entry,pid)
for s in model["surfaces"]:
    pivot = bpy.data.objects.new(s["id"],None)
    scene.collection.objects.link(pivot)
    pivot.empty_display_size = .24
    pivot["channel"] = s["channel"]
    center = metres(s["pv"])
    pivot.location = center
    if "parent" in s:
        pivot.parent = pivots[s["parent"]]
        pivot.location -= centers[s["parent"]]
    pivots[s["id"]] = pivot
    centers[s["id"]] = center
    axis = vector(s["ax"]).normalized()
    pivot.rotation_mode = "AXIS_ANGLE"
    for frame in range(1,182):
        angle = s["angle"]*travel(s,amount(s["channel"],frame))
        if s.get("rpm"):
            angle = math.tau*s["rpm"]/60*min(frame-1,80)/scene.render.fps
        pivot.rotation_axis_angle = (angle,*axis)
        pivot.keyframe_insert(data_path="rotation_axis_angle",frame=frame)
    for entry in s["e"]: mesh(entry,s["part"],pivot,s)

scene.frame_set(1)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/"models/blender/an225.blend"),compress=True)
export()
