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


class TodoApp(ft.UserControl):
    def __init__(self, client_storage, warning, page):
        super().__init__()
        self.client_storage = client_storage
        self.warning = warning
        self.warning.actions[0].on_click = self.close_clicked
        self.page = page

    def build(self):
        self.new_input = ft.TextField(hint_text="Write your task here", expand=True)
        self.new_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.create_clicked
        )
        self.input_row = ft.Row(controls=[self.new_input, self.new_button])

        self.tasks = ft.ListView(spacing=20, height=500)
        items = self.client_storage.get("items")
        if items is None:
            items = {}
        for item in items.keys():
            new_task = Task(item, self.task_delete)
            self.tasks.controls.append(new_task)

        self.view = ft.Column(controls=[self.input_row, self.tasks])
        self.view_container = ft.Container(content=self.view, padding=30)

        return self.view_container

    def create_clicked(self, event):
        task_name = self.new_input.value.strip()
        if task_name != "":
            items = self.client_storage.get("items")
            if items is None:
                items = {}
            if task_name in items:
                self.warning.title.value = "Duplicate"
                self.warning.content.value = "This item already exists"
                self.page.dialog = self.warning
                self.warning.open = True
                self.page.update()
            else:
                items[task_name] = False
                self.client_storage.set("items", items)
                new_task = Task(task_name, self.task_delete)
                self.tasks.controls.append(new_task)
                self.new_input.value = ""
                self.update()

    def close_clicked(self, event):
        self.warning.open = False
        self.page.update()

    def task_delete(self, task):
        items = self.client_storage.get("items")
        task_name = task.task_name
        items.pop(task_name)
        self.client_storage.set("items", items)
        self.tasks.controls.remove(task)
        self.update()

    def task_edit(self, task):
        pass   


def main(page: ft.Page):
    page.title = "Todo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    client_storage = page.client_storage
    warning = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[ft.ElevatedButton("OK")],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    todo = TodoApp(client_storage, warning, page)
    page.add(todo)
    page.update()


if __name__ == "__main__":
    ft.app(main)
