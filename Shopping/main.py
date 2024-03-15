import flet as ft


def main(page: ft.Page):
    # print(page.client_storage.get("lists"))
    def update_list_container(screen, listname=None):
        lists = page.client_storage.get("lists")
        if screen == "main":
            if lists is None:
                lists = dict()
            lists_container.controls = [
                ft.ResponsiveRow(
                    controls=[
                        ft.Text(value=listname, col={"xs": 4}),
                        ft.ElevatedButton(
                            text="Open",
                            on_click=lambda event, listname=listname: open_list(
                                event, listname
                            ),
                            col={"xs": 4},
                        ),
                        ft.ElevatedButton(
                            text="Delete",
                            on_click=lambda event, listname=listname: delete_list(
                                event, listname
                            ),
                            color="red",
                            col={"xs": 4},
                        ),
                    ]
                )
                for listname in lists.keys()
            ]
        else:
            items = lists[listname]
            second_title.value = listname
            new_item_button.on_click = lambda event, listname=listname: add_item(
                event, listname
            )
            lists_container.controls = [
                ft.ResponsiveRow(
                    controls=[
                        ft.Checkbox(
                            label=item[0],
                            on_change=lambda event, listname=listname, index=index: complete_item(
                                event, listname, index
                            ),
                            value=item[1],
                            col={"xs": 8}
                        ),
                        ft.ElevatedButton(
                            text="Delete",
                            on_click=lambda event, listname=listname, index=index: delete_item(
                                event, listname, index
                            ),
                            color="red",
                            col={"xs": 4},
                        ),
                    ]
                )
                for index, item in enumerate(items)
            ]
        page.update()

    def complete_item(event, listname, index):
        lists = page.client_storage.get("lists")
        lists[listname][index][1] = False if lists[listname][index][1] else True
        page.client_storage.set("lists", lists)
        update_list_container("second", listname)

    def open_warning(title, content):
        warning.title.value = title
        warning.content.value = content
        warning.open = True
        page.dialog = warning
        page.update()

    def open_confirm(title, content, listname, index=None):
        confirm.title.value = title
        confirm.content.value = content
        confirm.open = True
        if index is None:
            confirm.actions[0].on_click = (
                lambda event, listname=listname: delete_confirm_list(event, listname)
            )
        else:
            confirm.actions[0].on_click = (
                lambda event, listname=listname: delete_confirm_item(
                    event, listname, index
                )
            )
        page.dialog = confirm
        page.update()

    def add_list(event):
        listname = input_list_field.value
        if listname != "":
            lists = page.client_storage.get("lists")
            if lists is None:
                lists = dict()
            if listname in lists.keys():
                open_warning("Duplicate list", "There is already a list with this name")
            else:
                lists[listname] = []
                page.client_storage.set("lists", lists)
                update_list_container("main")
        else:
            open_warning("Empty name", "Name of list can't be empty")

    def add_item(event, listname):
        lists = page.client_storage.get("lists")
        items = lists[listname]
        if input_item_field.value != "":
            items.append((input_item_field.value, False))
            page.client_storage.set("lists", lists)
        update_list_container("second", listname)

    def open_list(event, listname):
        page.remove(main_container)
        page.add(second_container)
        update_list_container("second", listname)

    def delete_list(event, listname):
        open_confirm(
            "Delete list", "Are you sure you want to delete the list ?", listname
        )

    def delete_item(event, listname, index):
        open_confirm(
            "Delete item", "Are you sure you want to delete the item ?", listname, index
        )

    def delete_confirm_list(event, listname):
        lists = page.client_storage.get("lists")
        if lists is None:
            lists = dict()
        lists.pop(listname)
        page.client_storage.set("lists", lists)
        confirm.open = False
        update_list_container("main")

    def delete_confirm_item(event, listname, index):
        lists = page.client_storage.get("lists")
        lists[listname].pop(index)
        page.client_storage.set("lists", lists)
        confirm.open = False
        update_list_container("second", listname)

    def go_to_menu(event):
        page.remove(second_container)
        page.add(main_container)
        update_list_container("main")

    def close_alert(event, message):
        if message == "warning":
            warning.open = False
        elif message == "confirm":
            confirm.open = False
        page.update()

    lists_container = ft.Column(
        controls=[],
        scroll=True,
    )

    input_list_field = ft.TextField(
        label="Input list name", on_submit=add_list, col={"xs": 8}
    )
    input_item_field = ft.TextField(label="Input item name", col={"xs": 8})

    new_list_button = ft.ElevatedButton(text="Add", on_click=add_list, col={"xs": 4})
    new_item_button = ft.ElevatedButton(text="Add", col={"xs": 4})
    back_menu_button = ft.ElevatedButton(text="Go to lists", on_click=go_to_menu, col={"xs": 2})

    input_list_container = ft.ResponsiveRow(
        controls=[input_list_field, new_list_button]
    )
    input_item_container = ft.ResponsiveRow(
        controls=[input_item_field, new_item_button]
    )

    main_title = ft.Text(
        value="My Lists",
        size=32,
        weight=ft.FontWeight.BOLD,
    )

    second_title = ft.Text(
        value="",
        size=32,
        weight=ft.FontWeight.BOLD,
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[main_title, lists_container, input_list_container],
        )
    )

    second_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=[back_menu_button, second_title]),
                lists_container,
                input_item_container,
            ],
        )
    )

    warning = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[
            ft.TextButton("OK", on_click=lambda event: close_alert(event, "warning")),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    confirm = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[
            ft.ElevatedButton("OK", bgcolor="white"),
            ft.TextButton(
                "Cancel", on_click=lambda event: close_alert(event, "confirm")
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.window_center()
    page.add(main_container)
    update_list_container("main")


ft.app(main)
