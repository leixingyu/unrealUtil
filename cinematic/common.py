import os

import unreal


def set_binding_cam_anim(fbx, u_binding):
    """
    Import .fbx animation on camera binding track

    :param fbx: str. camera .fbx path
    :param u_binding: unreal.SequencerBindingProxy
    """
    settings = unreal.MovieSceneUserImportFBXSettings()
    settings.set_editor_property('create_cameras', False)
    settings.set_editor_property('force_front_x_axis', False)
    settings.set_editor_property('match_by_name_only', False)
    settings.set_editor_property('reduce_keys', False)

    u_seq = u_binding.get_editor_property('sequence')
    u_world = unreal.EditorLevelLibrary.get_editor_world()
    unreal.SequencerTools.import_level_sequence_fbx(
        u_world,
        u_seq,
        [u_binding],
        settings,
        fbx
    )


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
    options.set_editor_property('mesh_type_to_import', unreal.FBXImportType.FBXIT_ANIMATION)

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
