import os

import unreal


def create_anim_seq(fbx, anim_seq_path, u_skeleton):
    """
    Create an Animation Sequence from a .fbx and unreal skeleton

    :param fbx: str. animation .fbx path
    :param anim_seq_path: str. path to the newly created animation sequence
                               asset
    :param u_skeleton: unreal.Skeleton.
    """
    options = unreal.FbxImportUI()
    options.set_editor_property('skeleton', u_skeleton)
    options.set_editor_property('automated_import_should_detect_type', False)
    options.set_editor_property(
        'mesh_type_to_import',
        unreal.FBXImportType.FBXIT_ANIMATION)

    options.set_editor_property('import_animations', True)
    options.set_editor_property('import_as_skeletal', True)
    options.set_editor_property('import_rigid_mesh', False)
    options.set_editor_property('import_mesh', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('create_physics_asset', False)

    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('filename', fbx)
    task.set_editor_property('destination_name', os.path.basename(fbx))
    task.set_editor_property('destination_path', anim_seq_path)
    task.set_editor_property('options', options)
    task.set_editor_property('save', True)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
