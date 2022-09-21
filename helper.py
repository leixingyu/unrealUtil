import os

import unreal


def normalize_path(path):
    """
    Normalize path to Unreal readable format

    :param path: str. original path
    :return: str. formatted path
    """
    return os.path.normpath(path).replace('\\', '/')


def get_selected_asset():
    """
    Get selected assets in content browser

    :return: [unreal.Object].
    """
    return unreal.EditorUtilityLibrary.get_selected_assets()


def get_asset(path):
    """
    Get asset of a Unreal path

    :param path: str. relative Unreal path
    :return: unreal.Object
    """
    return unreal.EditorAssetLibrary.find_asset_data(path).get_asset()


def get_assets_from_folder(folder):
    """
    Get certain types of assets from a directory

    :param folder: str. search directory
    :return: [unreal.Object].
    """
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    asset_datas = asset_registry.get_assets_by_path(folder)

    return [asset_data.get_asset() for asset_data in asset_datas]


def filter_assets(assets, typ):
    """
    Filter to get certain type of Unreal asset

    :param assets: [unreal.Object]. list of assets to filter
    :param typ: unreal.Class. asset type to filter
    :return: [unreal.Object].
    """
    return [asset for asset in assets if isinstance(asset, typ)]


def create_folder(root, name):
    """
    Create a Unreal sub folder

    :param root: str. directory root
    :param name: str. Unreal folder name
    :return: bool. whether the creation is successful
    """
    path = os.path.join(root, name)
    return unreal.EditorAssetLibrary.make_directory(path)


def get_actor(label):
    """
    Get actor from label in the current level/world

    this can't get all actors:
    `actors = unreal.EditorActorSubsystem().get_all_level_actors()`

    :param label: str. display label (different from actor name)
    :return: unreal.Actor
    """
    actors = unreal.GameplayStatics.get_all_actors_of_class(
        unreal.EditorLevelLibrary.get_editor_world(),
        unreal.Actor)

    matches = [actor for actor in actors if label == actor.get_actor_label()]
    if not matches:
        return None
    else:
        return matches[0]
