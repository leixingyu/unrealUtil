"""
Unreal Menu Utility

There are three components to a Unreal Menu

1. Tool Menu:
    this is the container for storing tool entries and tool menus (sub-menu)
2. Tool Menu Entry
    this is the root of the menu 'tree', it execute certain operation
3. Tool Menu Section
    this is a divider in tool menu for organizing tool entries and tool menus
    (totally optional)

Note:
    an important thing to note is that 'name' refers to the internal Unreal
    object name, whereas 'label' refers to the display name in the editor
"""


from functools import wraps


import unreal


def refresh_menus(func):
    """
    Force a post-refresh on Unreal main menu bar
    """
    @wraps(func)
    def refresh(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise
        finally:
            menus = unreal.ToolMenus.get()
            menus.refresh_all_widgets()

    return refresh


def get_menu_bar(menu_name='LevelEditor.MainMenu'):
    """
    Get Unreal Menu Bar

    :param menu_name: str. menu object name, default to 'LevelEditor.MainMenu'
                      which is the Unreal Main Menu Bar
    :return: unreal.ToolMenu.
    """
    menus = unreal.ToolMenus.get()
    menu_bar = menus.find_menu(menu_name)

    if not menu_bar:
        return None

    return menu_bar


def create_menu(parent_menu, menu_name, section_name=''):
    """
    Create a submenu

    :param parent_menu: unreal.ToolMenu. menu to be created in
    :param menu_name: str. name of the submenu
    :param section_name: str. (Optional) name of the menu section
    :return: unreal.ToolMenu
    """
    sub_menu = parent_menu.add_sub_menu(
        owner=parent_menu.get_name(),
        section_name=section_name,
        name=menu_name,
        label=menu_name
    )
    return sub_menu


def create_menu_section(parent_menu, section_name=''):
    """
    Create a menu section, for organizing menu entry or submenu

    :param parent_menu: unreal.ToolMenu. menu to be created in
    :param section_name: str. (Optional) name of the menu section
    :return: str. name of the menu section created
    """
    parent_menu.add_section(section_name=section_name, label=section_name)
    return section_name


def create_menu_entry(parent_menu, entry_name, command, section_name=''):
    """
    Create a menu entry

    :param parent_menu: unreal.ToolMenu. menu to be created in
    :param entry_name: str. menu entry name
    :param command: str. python command to execute
    :param section_name: str. (Optional) name of the menu section
    :return: unreal.ToolMenuEntry
    """
    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.MENU_ENTRY)
    entry.set_label(entry_name)
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=command
    )
    parent_menu.add_menu_entry(section_name, entry)
    return entry


def create_tool_button(parent_menu, entry_name, command, section_name=''):
    """
    Create a menu tool bar button

    :param parent_menu: unreal.ToolMenu. menu to be created in
    :param entry_name: str. menu entry name
    :param command: str. python command to execute
    :param section_name: str. (Optional) name of the menu section
    :return: unreal.ToolMenuEntry
    """
    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(entry_name)
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=command
    )
    parent_menu.add_menu_entry(section_name, entry)
    return entry


def list_menu(num=1000):
    """
    Query all menu object name

    https://blog.l0v0.com/posts/cad78e0d.html

    :param num: int. menu object max count
    :return: [str]. list of menu object names
    """
    menu_list = set()
    for i in range(num):
        obj = unreal.find_object(
            None,
            "/Engine/Transient.ToolMenus_0:RegisteredMenu_%s" % i
        )
        if not obj:
            continue

        menu_name = str(obj.menu_name)
        if menu_name != "None":
            menu_list.add(menu_name)

    return list(menu_list)
