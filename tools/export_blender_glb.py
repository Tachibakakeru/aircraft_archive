"""Export an opened Blender source as a reusable GLB under models/glb/."""
from pathlib import Path

import bpy


def export():
    source = Path(bpy.data.filepath)
    assert source.suffix == '.blend' and source.parent.name == 'blender', source
    destination = source.parent.parent / 'glb' / source.with_suffix('.glb').name
    destination.parent.mkdir(exist_ok=True)
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)
    result = bpy.ops.export_scene.gltf(
        filepath=str(destination),
        export_format='GLB',
        export_extras=True,
        export_animation_mode='SCENE',
        export_anim_scene_split_object=False,
        export_frame_range=True,
    )
    assert 'FINISHED' in result and destination.stat().st_size > 0, result
    print(f'Exported {destination.name}: {destination.stat().st_size:,} bytes')


if __name__ == '__main__':
    export()
