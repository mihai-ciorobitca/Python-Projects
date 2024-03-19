import flet as ft


class Task(ft.UserControl):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        item_checkbox = ft.Checkbox(label=self.task_name, expand=True)
        item_delete = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE_OUTLINED, on_click=self.delete_clicked
        )
        item_edit = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit_clicked)

        task_row = ft.Row(controls=[item_checkbox, item_edit, item_delete])
        return task_row

    def delete_clicked(self, event):
        self.task_delete(self)

    def edit_clicked(self, event):
        self.task_edit(self)


class List(ft.UserControl):
    def __init__(self, list_name, list_delete, list_open, list_edit):
        super().__init__()
        self.list_name = list_name
        self.list_delete = list_delete
        self.list_open = list_open
        self.list_edit = list_edit

        self.text_element = ft.TextField(
            value=self.list_name, expand=True, border="none", read_only=True
        )
        self.delete_element = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE_OUTLINED, on_click=self.delete_clicked
        )
        self.open_element = ft.IconButton(
            icon=ft.icons.OPEN_IN_BROWSER_OUTLINED, on_click=self.open_clicked
        )
        self.edit_element = ft.IconButton(
            icon=ft.icons.EDIT, on_click=self.edit_clicked
        )
        self.save_element = ft.IconButton(
            icon=ft.icons.SAVE, on_click=self.save_clicked, visible=False
        )
        self.cancel_element = ft.IconButton(
            icon=ft.icons.CANCEL, on_click=self.cancel_clicked, visible=False
        )

    def build(self):
        list_row = ft.Row(
            controls=[
                self.text_element,
                self.delete_element,
                self.open_element,
                self.edit_element,
                self.save_element,
                self.cancel_element,
            ]
        )
        return list_row

    def delete_clicked(self, event):
        self.list_delete(self)

    def save_clicked(self, event):
        pass

    def cancel_clicked(self, event):
        pass

    def open_clicked(self, event):
        self.list_open(self.list_name)

    def edit_clicked(self, event):
        self.text_element.read_only = False
        self.text_element.border = "solid"
        self.delete_element.visible = False
        self.open_element.visible = False
        self.edit_element.visible = False
        self.save_element.visible = True
        self.cancel_element.visible = True
        self.update()


class ListPage(ft.UserControl):
    def __init__(self, client_storage, warning, page, list_name):
        super().__init__()
        self.client_storage = client_storage
        self.warning = warning
        self.warning.actions[0].on_click = self.close_clicked
        self.page = page
        self.list_name = list_name
        self.page.title = self.list_name.upper()

    def build(self):
        self.home_button = ft.FloatingActionButton(
            icon=ft.icons.HOME, on_click=self.home_clicked
        )
        self.new_input = ft.TextField(hint_text="Write your task here", expand=True)
        self.new_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.create_clicked
        )
        self.input_row = ft.Row(
            controls=[self.home_button, self.new_input, self.new_button]
        )

        self.tasks = ft.ListView(spacing=20, height=500)
        lists = self.client_storage.get("lists")
        items = lists.get(self.list_name)
        for item in items.keys():
            new_task = Task(item, self.task_delete)
            self.tasks.controls.append(new_task)

        self.view = ft.Column(controls=[self.input_row, self.tasks])
        self.view_container = ft.Container(content=self.view, padding=30)

        return self.view_container

    def create_clicked(self, event):
        task_name = self.new_input.value.strip()
        if task_name != "":
            lists = self.client_storage.get("lists")
            items = lists.get(self.list_name)
            if task_name in items:
                self.warning.title.value = "Duplicate"
                self.warning.content.value = "This item already exists"
                self.page.dialog = self.warning
                self.warning.open = True
                self.page.update()
            else:
                items[task_name] = False
                self.client_storage.set("lists", lists)
                new_task = Task(task_name, self.task_delete)
                self.tasks.controls.append(new_task)
                self.new_input.value = ""
                self.update()

    def close_clicked(self, event):
        self.warning.open = False
        self.page.update()

    def task_delete(self, task):
        lists = self.client_storage.get("lists")
        items = lists.get(self.list_name)
        task_name = task.task_name
        items.pop(task_name)
        self.client_storage.set("lists", lists)
        self.tasks.controls.remove(task)
        self.update()

    def task_edit(self, task):
        pass

    def home_clicked(self, event):
        main_page = MainPage(self.client_storage, self.warning, self.page)
        self.page.controls.remove(self)
        self.page.title = "TODO APP"
        self.page.add(main_page)


class MainPage(ft.UserControl):
    def __init__(self, client_storage, warning, page):
        super().__init__()
        self.client_storage = client_storage
        self.warning = warning
        self.warning.actions[0].on_click = self.close_clicked
        self.page = page

    def build(self):
        self.new_input = ft.TextField(hint_text="Create a list", expand=True)
        self.new_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.create_clicked
        )
        self.input_row = ft.Row(controls=[self.new_input, self.new_button])

        self.lists = ft.ListView(spacing=20, height=500)
        lists = self.client_storage.get("lists")
        if lists is None:
            lists = {}
        for list in lists.keys():
            new_list = List(list, self.list_delete, self.list_open, self.list_edit)
            self.lists.controls.append(new_list)

        self.view = ft.Column(controls=[self.input_row, self.lists])
        self.view_container = ft.Container(content=self.view, padding=30)

        return self.view_container

    def create_clicked(self, event):
        list_name = self.new_input.value.strip()
        if list_name != "":
            items = self.client_storage.get("lists")
            if items is None:
                items = {}
            if list_name in items:
                self.warning.title.value = "Duplicate"
                self.warning.content.value = "This list already exists"
                self.page.dialog = self.warning
                self.warning.open = True
                self.page.update()
            else:
                items[list_name] = {}
                self.client_storage.set("lists", items)
                new_list = List(list_name, self.list_delete, self.list_open)
                self.lists.controls.append(new_list)
                self.new_input.value = ""
                self.update()
        else:
            self.warning.title.value = "Empty"
            self.warning.content.value = "List name can't be empty"
            self.page.dialog = self.warning
            self.warning.open = True
            self.page.update()

    def close_clicked(self, event):
        self.warning.open = False
        self.page.update()

    def list_delete(self, list):
        items = self.client_storage.get("lists")
        list_name = list.list_name
        items.pop(list_name)
        self.client_storage.set("lists", items)
        self.tasks.controls.remove(list)
        self.update()

    def list_open(self, list_name):
        list_page = ListPage(self.client_storage, self.warning, self.page, list_name)
        self.page.controls.remove(self)
        self.page.add(list_page)

    def list_edit(self, list):
        pass


def main(page: ft.Page):

    page.title = "TODO APP"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    client_storage = page.client_storage
    warning = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[ft.ElevatedButton("OK")],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    main_page = MainPage(client_storage, warning, page)
    page.add(main_page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
