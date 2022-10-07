import os

import unreal


SYS_ROOT = unreal.SystemLibrary.convert_to_absolute_path(
    unreal.Paths.project_content_dir())
UNREAL_ROOT = '/Game/'


def normalize_path(path):
    """
    Normalize path string to an uniform format that Unreal can read

    :param path: str. input path of directory/folder
    :return: str. formatted path
    """
    return os.path.normpath(path).replace('\\', '/')


def is_unreal_path(path):
    """
    Determines if path string is an relative Unreal path

    :param path: str. input path of directory/folder
    :return: bool. whether the path is an Unreal path
    """
    path = normalize_path(path)

    return True if UNREAL_ROOT in path else False


def is_sys_path(path):
    """
    Determines if path string is an absolute system path

    :param path: str. input path of directory/folder
    :return: bool. whether the path is a system path
    """
    path = normalize_path(path)

    return True if SYS_ROOT in path else False


def to_unreal_path(path):
    """
    Format an absolute system path to a relative Unreal path, the path can
    either be a directory or a file.

    Example:
        file:
            in: "C:/Users/Lei/Desktop/UnrealProj/SequencerTest/Content/Cinematics/MetaHuman.uasset"
            out: "/Game/Cinematics/MetaHuman.MetaHuman"
        directory:
            in: "C:/Users/Lei/Desktop/UnrealProj/SequencerTest/Content/Cinematics"
            out: "/Game/Cinematics"


    :param path: str. input path of directory/folder
    :return: str. path in Unreal format
    """
    if is_unreal_path(path):
        return normalize_path(path)

    path = normalize_path(path)

    if os.path.isfile(path):
        no_extension_path = os.path.splitext(path)[0]
        root = no_extension_path.split(SYS_ROOT)[-1]
        path = os.path.join(UNREAL_ROOT, root)
        asset = unreal.EditorAssetLibrary.find_asset_data(path).get_asset()
        return asset.get_path_name()

    root = path.split(SYS_ROOT)[-1]
    return os.path.join(UNREAL_ROOT, root)


def to_sys_path(path):
    """
    Format a relative unreal path to an absolute system path, the path can
    either be a directory or a file.

    Example:
        file:
            in: "/Game/Cinematics/MetaHuman.MetaHuman"
            out: "C:/Users/Lei/Desktop/UnrealProj/SequencerTest/Content/Cinematics/MetaHuman.uasset"
        directory:
            in: "/Game/Cinematics"
            out: "C:/Users/Lei/Desktop/UnrealProj/SequencerTest/Content/Cinematics"

    :param path: str. input path of directory/folder
    :return: str. path in system format
    """
    if is_sys_path(path):
        return normalize_path(path)

    path = normalize_path(path)

    # symbol '.' is not allowed in regular Unreal path
    # thus this determines a path points to an asset not a folder
    if '.' in path:
        no_extension_path = os.path.splitext(path)[0]
        root = no_extension_path.split(UNREAL_ROOT)[-1]
        return os.path.join(SYS_ROOT, root+'.uasset')

    root = path.split(UNREAL_ROOT)[-1]
    return os.path.join(SYS_ROOT, root)
