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


def get_menu_bar(menu_type='LevelEditor.MainMenu'):
    menus = unreal.ToolMenus.get()
    menu_bar = menus.find_menu(menu_type)

    if not menu_bar:
        unreal.log_error(
            'Failed to find toolbar, Unreal did not load properly'
        )
        return None

    return menu_bar


def create_menu(parent_menu, menu_name):
    sub_menu = parent_menu.add_sub_menu(
        owner=parent_menu.get_name(),
        section_name=menu_name,
        name=menu_name,
        label=menu_name
    )
    return sub_menu


def create_menu_section(parent_menu, section_name):
    parent_menu.add_section(
        section_name=section_name,
        label=section_name,
        insert_name=section_name,
        insert_type=unreal.ToolMenuInsertType.DEFAULT
    )
    return section_name


def create_menu_entry(parent_menu, section_name, entry_name, command):
    entry = unreal.ToolMenuEntry(
        name=entry_name,
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert(
            name='',
            position=unreal.ToolMenuInsertType.DEFAULT
        )
    )
    entry.set_label(entry_name)
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=command
    )

    parent_menu.add_menu_entry(section_name, entry)


def create_toolbar_entry(parent_menu, section_name, entry_name, command):
    entry = unreal.ToolMenuEntry(
        type=unreal.MultiBlockType.TOOL_BAR_BUTTON,
    )
    entry.set_label(entry_name)
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type='',
        string=command
    )

    parent_menu.add_menu_entry(section_name, entry)


def list_menu(num=1000):
    # https://blog.l0v0.com/posts/cad78e0d.html

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
