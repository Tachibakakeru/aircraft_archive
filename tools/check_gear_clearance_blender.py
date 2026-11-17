"""Sample the full slider travel for gear/door mesh intersections in Blender.

blender -b models/blender/dreamlifter.blend --python-exit-code 1 --python tools/check_gear_clearance_blender.py
Also supports models/blender/a321neo.blend.
"""
import math
from itertools import combinations

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def check():
    scene = bpy.context.scene
    meshes = [ob for ob in scene.objects if ob.type == 'MESH']
    doors = [ob for ob in meshes if '_door_' in ob.get('joint', '')]
    gear = [ob for ob in meshes if ob.get('partId') == 'gear' and ob not in doors]
    assert doors and gear, 'No gear or door rig found'
    faces = {ob: [tuple(face.vertices) for face in ob.data.polygons] for ob in meshes}

    def tree(ob):
        points = [ob.matrix_world @ vertex.co for vertex in ob.data.vertices]
        return BVHTree.FromPolygons(points, faces[ob])

    pairs = [(door, ob) for door in doors for ob in gear]
    a321neo = bpy.data.objects.get('A321neo pressure shell')
    if a321neo:
        shell = [ob for ob in meshes if ob == a321neo or ob.name.startswith(
            ('Wing-body and main gear fairing', 'Wing box', 'Fixed inboard trailing edge',
             'Fixed main wheel bay shoulder'))]
        wheels = [ob for ob in gear if ' tyre' in ob.name or ' hub' in ob.name]
        flaps = [ob for ob in meshes if ob.name.startswith('Flap ')]
        tracks = [ob for ob in meshes if 'flap track fairing' in ob.name]
        assert wheels and flaps and tracks
        pairs += [(ob, wheel) for ob in shell for wheel in wheels]
        pairs += [(track, flap) for track in tracks for flap in flaps]
        pairs += list(combinations([door for door in doors if 'main_door_' in door.get('joint','')], 2))

    objects = {ob for pair in pairs for ob in pair}
    fixed = {ob: tree(ob) for ob in objects if not ob.get('joint')}
    collisions = {}
    for step in range(401):
        frame = scene.frame_start + (scene.frame_end - scene.frame_start) * step / 400
        scene.frame_set(int(frame), subframe=frame - int(frame))
        trees = fixed | {ob: tree(ob) for ob in objects - fixed.keys()}
        for a, b in pairs:
            if trees[a].overlap(trees[b]):
                hit = collisions.setdefault((a.name, b.name), [step, step])
                hit[1] = step
    assert not collisions, '\n'.join(f'{a} vs {b}: {lo/400:.3f}–{hi/400:.3f}'
                                     for (a, b), (lo, hi) in collisions.items())
    print(f'Gear clearance OK: {len(doors)} door panels, {len(gear)} other gear meshes, 401 poses')
    if a321neo:
        for name, limit in [('aileron_L',23), ('aileron_R',23), ('elevator_L',27),
                            ('elevator_R',27), ('rudder',27)]:
            actual = math.degrees(bpy.data.objects[name].rotation_axis_angle[0])
            assert math.isclose(abs(actual), limit, abs_tol=.001), (name, actual, limit)
        lower_skin = [trees[ob] for ob in shell + doors]
        down = Vector((0, 0, -1))
        for wheel in wheels:
            for vertex in wheel.data.vertices:
                point = wheel.matrix_world @ vertex.co
                assert any(panel.ray_cast(point, down)[0] is not None for panel in lower_skin), (
                    'Exposed stowed wheel below skin', wheel.name, tuple(point))
        shoulders = [trees[ob] for ob in shell if ob.name.startswith('Fixed main wheel bay shoulder')]
        outer_doors = [trees[ob] for ob in doors if ob.name.startswith('outer_main_door_')]
        if shoulders or outer_doors:
            assert len(shoulders) == len(outer_doors) == 2
            for x in (-.32,.25,.85):
                for y in (-2.82,-2.49,-2.11,2.11,2.49,2.82):
                    assert any(ob.ray_cast(Vector((x,y,4)),down)[0] is not None for ob in shoulders), (
                        'Open wing root over the main wheel bay', x, y)
                    assert any(ob.ray_cast(Vector((x,y,1)),-down)[0] is not None for ob in outer_doors), (
                        'Uncovered portion of outer main wheel bay', x, y)
        print(f'A321neo clearance OK: {len(wheels)} wheel meshes, {len(shell)} shell meshes, '
              f'{len(flaps)} flap elements, {len(tracks)} track fairing segments, 401 poses')


if __name__ == '__main__':
    check()
