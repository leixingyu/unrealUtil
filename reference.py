"""
Find Unreal asset's referencers or dependencies

Similar backend behaviour compared to Unreal's reference viewer
"""


def get_references_as_list(
        u_registry,
        u_options,
        u_asset,
        search_depth,
        filter_code=True,
        remove_duplicate=True,
        duplicate_lookups=list()
):
    """
    Get asset referencer as a nested list
    return list needs to be flattened if the desired outcome is referenced assets not considering the reference level

    :param u_registry: unreal.AssetRegistry
    :param u_options: unreal.AssetRegistryReferenceOption
    :param u_asset: str. unreal asset package name (the outer name. e.g. /Game/Main and not /Game/Main.Main)
    :param search_depth: int. reference search depth level
    :param filter_code: bool. whether to filter out engine builtin script or functions etc
    :param remove_duplicate: bool. whether to remove duplicated asset reference
    :param duplicate_lookups: list. use for internal storage to check up duplicated asset reference
    :return: nested[str]. nested list in which each nested level is the reference level,
                          each element is a string representing the unreal path referencing the current asset
    """
    storages = [u_asset]
    references = u_registry.get_referencers(
        package_name=u_asset,
        reference_options=u_options
    )

    if filter_code:
        references = [ref for ref in references
                      if str(ref).startswith('/Game')]

    if remove_duplicate:
        references = [ref for ref in references
                      if ref not in duplicate_lookups]

    if references:
        if search_depth == 1:
            storages.append(references)
        else:
            for asset in references:
                # need to go deeper
                child_references = get_references_as_list(
                    u_registry,
                    u_options,
                    asset,
                    search_depth - 1
                )
                duplicate_lookups.extend(child_references)
                storages.append(child_references)

    return storages


def get_references(
        u_registry,
        u_options,
        u_asset,
        search_depth=99,
        filter_code=True,
        remove_duplicate=True,
        duplicate_lookups=list()
    ):
    """
    Get asset referencer as a nested dictionary

    :param u_registry: unreal.AssetRegistry
    :param u_options: unreal.AssetRegistryReferenceOption
    :param u_asset: str. unreal asset package name (the outer name. e.g. /Game/Main and not /Game/Main.Main)
    :param search_depth: int. reference search depth level
    :param filter_code: bool. whether to filter out engine builtin script or functions etc
    :param remove_duplicate: bool. whether to remove duplicated asset reference
    :param duplicate_lookups: list. use for internal storage to check up duplicated asset reference
    :return: nested{str: list[str]}. nested dictionary in which each nested level is the reference level,
                                     key representing current asset unreal path,
                                     value representing the referencer(s) unreal path
    """
    storages = {u_asset: dict()}

    references = u_registry.get_referencers(
        package_name=u_asset,
        reference_options=u_options
    )

    if filter_code:
        references = [ref for ref in references
                      if str(ref).startswith('/Game')]

    if remove_duplicate:
        references = [ref for ref in references
                      if ref not in duplicate_lookups]

    if references:
        duplicate_lookups.extend(references)

        if search_depth == 1:
            for asset in references:
                storages[u_asset][asset] = None
        else:
            for asset in references[:]:
                # need to go deeper
                storages[u_asset][asset] = get_references(
                    u_registry,
                    u_options,
                    asset,
                    search_depth - 1,
                    filter_code,
                    remove_duplicate,
                    duplicate_lookups
                )
                references = u_registry.get_referencers(
                    package_name=asset,
                    reference_options=u_options
                )
                duplicate_lookups.extend(references)

    return storages


def get_dependencies_as_list(
        u_registry,
        u_options,
        u_asset,
        search_depth=99,
        filter_code=True,
        remove_duplicate=True,
        duplicate_lookups=list()
):
    """
    Get asset dependencies as a nested list
    return list needs to be flattened if the desired outcome is referenced assets not considering the dependency level

    :param u_registry: unreal.AssetRegistry
    :param u_options: unreal.AssetRegistryDependencyOption
    :param u_asset: str. unreal asset package name (the outer name. e.g. /Game/Main and not /Game/Main.Main)
    :param search_depth: int. dependency search depth level
    :param filter_code: bool. whether to filter out engine builtin script or functions etc
    :param remove_duplicate: bool. whether to remove duplicated asset dependency
    :param duplicate_lookups: list. use for internal storage to check up duplicated asset dependency
    :return: nested[str]. nested list in which each nested level is the dependency level,
                          each element is a string representing the unreal path dependencies of the current asset
    """
    storages = [u_asset]
    dependencies = u_registry.get_dependencies(
        package_name=u_asset,
        dependency_options=u_options
    )

    if filter_code:
        dependencies = [dep for dep in dependencies
                        if str(dep).startswith('/Game')]

    if remove_duplicate:
        dependencies = [dep for dep in dependencies
                        if dep not in duplicate_lookups]

    if dependencies:
        duplicate_lookups.extend(dependencies)
        if search_depth == 1:
            storages.append(dependencies)
        else:
            for asset in dependencies:
                # need to go deeper
                child_dependencies = get_dependencies_as_list(
                    u_registry,
                    u_options,
                    asset,
                    search_depth - 1
                )
                duplicate_lookups.extend(child_dependencies)
                storages.append(child_dependencies)

    return storages


def get_dependencies(
        u_registry,
        u_options,
        u_asset,
        search_depth=99,
        filter_code=True,
        remove_duplicate=True,
        duplicate_lookups=list()
):
    """
    Get asset dependencies as a nested list
    return list needs to be flattened if the desired outcome is referenced assets not considering the dependency level

    :param u_registry: unreal.AssetRegistry
    :param u_options: unreal.AssetRegistryDependencyOption
    :param u_asset: str. unreal asset package name (the outer name. e.g. /Game/Main and not /Game/Main.Main)
    :param search_depth: int. dependency search depth level
    :param filter_code: bool. whether to filter out engine builtin script or functions etc
    :param remove_duplicate: bool. whether to remove duplicated asset dependency
    :param duplicate_lookups: list. use for internal storage to check up duplicated asset dependency
    :return: nested{str: list[str]}. nested dictionary in which each nested level is the dependency level,
                                     key representing current asset unreal path,
                                     value representing the dependency(s) unreal path
    """
    storages = {u_asset: dict()}

    dependencies = u_registry.get_dependencies(
        package_name=u_asset,
        dependency_options=u_options
    )

    if filter_code:
        dependencies = [dep for dep in dependencies
                        if str(dep).startswith('/Game')]

    if remove_duplicate:
        dependencies = [dep for dep in dependencies
                        if dep not in duplicate_lookups]

    if dependencies:
        duplicate_lookups.extend(dependencies)

        if search_depth == 1:
            for asset in dependencies:
                storages[u_asset][asset] = None
        else:
            for asset in dependencies[:]:
                # need to go deeper
                storages[u_asset][asset] = get_dependencies(
                    u_registry,
                    u_options,
                    asset,
                    search_depth - 1,
                    filter_code,
                    remove_duplicate,
                    duplicate_lookups
                )
                dependencies = u_registry.get_dependencies(
                    package_name=asset,
                    dependency_options=u_options
                )
                duplicate_lookups.extend(dependencies)

    return storages
