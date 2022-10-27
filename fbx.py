import os

import unreal


def import_binding_cam_fbx(fbx, u_binding):
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


def reimport_fbx(u_asset):
    """
    Re-import Unreal uasset with same import options

    :param u_asset: unreal.Object. unreal asset
    :return: unreal.Object
    """
    import_data = u_asset.get_editor_property('asset_import_data')
    fbx_file = import_data.get_first_filename()

    task = unreal.AssetImportTask()
    task.set_editor_property('destination_path',
                             u_asset.get_path_name().rpartition("/")[0])
    task.set_editor_property('destination_name', u_asset.get_name())
    task.set_editor_property('filename', fbx_file)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    return u_asset


def import_skm_fbx(fbx_file, u_folder, name):
    """
    Create Skeletal Mesh components/assets: Skeletal Mesh, Skeleton and
    Physics Asset.

    :param fbx_file: str. source .fbx file
    :param u_folder: str. Unreal directory to store the created assets
    :param name: str. name of the created asset
    """
    skm_name = os.path.basename(os.path.splitext(fbx_file)[0])
    u_asset_file = os.path.join(u_folder, skm_name)

    if unreal.EditorAssetLibrary.does_asset_exist(u_asset_file):
        unreal.log_error('Asset %s already exists', u_asset_file)
        return None

    options = unreal.FbxImportUI()
    options.automated_import_should_detect_type = False
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    options.import_animations = False
    options.import_as_skeletal = True
    options.import_materials = False
    options.import_textures = False
    options.create_physics_asset = True

    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_path', u_folder)
    task.set_editor_property('destination_name', name)
    task.set_editor_property('filename', fbx_file)
    task.set_editor_property('options', options)
    task.set_editor_property('save', True)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])


def import_anim_fbx(fbx_file, u_skeleton, u_folder, name):
    """
    Create an Animation Sequence from a .fbx and unreal skeleton

    :param fbx_file: str. animation .fbx path
    :param u_skeleton: unreal.Skeleton.
    :param u_folder: str. path to the newly created animation sequence
                           asset
    :param name: str. name of the created asset
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
    task.set_editor_property('destination_path', u_folder)
    task.set_editor_property('filename', fbx_file)
    task.set_editor_property('destination_name', name)
    task.set_editor_property('options', options)
    task.set_editor_property('save', True)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
