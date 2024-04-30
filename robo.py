import flet as ft
import pyautogui
import time

class TodoApp(ft.UserControl):
    def build(self):
        self.comands = ft.Dropdown(
            width=200,
            label='Ação',
            on_change=self.change_task,
            options=[
                ft.dropdown.Option("Escrever"),
                ft.dropdown.Option("Mover mouse"),
                ft.dropdown.Option("Click"),
                ft.dropdown.Option("Duplo Click"),
                ft.dropdown.Option("Pressionar tecla"),
                ft.dropdown.Option("Esperar")
            ]
        )
        self.new_task = ft.TextField(label="Tarefa", visible=True, expand=True)
        self.coordX = ft.TextField(label="X",visible=True, width=80)
        self.coordY = ft.TextField(label="Y",visible=True, width=80)
        self.repeticoes = ft.TextField(label="Quantidade de execuções",visible=False, width=200)

        self.view_task = ft.Row(
            visible=True,
            expand=True,
            controls=[
                self.new_task
            ]
        )
        self.display_coordenadas = ft.Row(
            visible=False,
            controls=[
                self.coordX,
                self.coordY
            ]
        )
        
        self.tasks = ft.Column()
        
        return ft.Column(
            width=600,
            height=700,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Row(
                    controls=[
                        self.comands,
                        self.view_task,
                        self.display_coordenadas,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
                self.repeticoes,
                ft.ElevatedButton(text='Executar automação', on_click=self.executarrobo)
            ],
        )

    def change_task(self,e):
        if self.comands.value == 'Mover mouse':
            self.display_coordenadas.visible = True
            self.view_task.visible = False
            self.update()
        else:
            self.display_coordenadas.visible = False
            self.view_task.visible = True
            self.update()

    def add_clicked(self, e):
        if self.coordX.value != '' and self.coordY.value != '':
            task = Task(f'{self.comands.value}|' + self.coordX.value + '|' + self.coordY.value, self.task_delete)
        else:
            task = Task(f'{self.comands.value}|' + self.new_task.value, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.coordX.value = ""
        self.coordY.value = ""
        self.repeticoes.visible = True
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    

    def executarrobo(self, e):
        interacoes = int(self.repeticoes.value)
        pyautogui.FAILSAFE = True
        for y in range(interacoes):
            for i in range(len(self.tasks.controls)):
                conteudo = self.tasks.controls[i].controls[0].controls[0].controls[0].label
                conteudo = conteudo.split('|')
                if conteudo[0] == 'Escrever':
                    pyautogui.write(str(conteudo[1]), interval=0.25)
                elif conteudo[0] == 'Mover mouse':
                    pyautogui.moveTo(int(conteudo[1]),int(conteudo[2]), duration=1)
                elif conteudo[0] == 'Click':
                    pyautogui.click()
                elif conteudo[0] == 'Duplo Click':
                    pyautogui.doubleClick()
                elif conteudo[0] == 'Pressionar tecla':
                    pyautogui.press(str(conteudo[1]), interval=0.25)
                elif conteudo[0] == 'Esperar':
                    time.sleep(int(conteudo[1]))
                
        

class Task(ft.UserControl):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Checkbox(value=False, label=self.task_name)
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Editar tarefa",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Deletar tarefa",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Atualizar tarefa",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)
        
    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()


def main(page: ft.Page):
    
    def on_enter(e: ft.KeyboardEvent):
        if e.key == 'Enter':
            x, y = pyautogui.position()
            page.snack_bar = ft.SnackBar(
                ft.Text(value=f'X={x} Y={y}')
            )
            page.snack_bar.open = True
            page.update()

    def mudar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    page.title = "Automação de tarefas"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(
        title=ft.Text(value='Automação', weight=True, size=22),
        center_title=True,
        actions=[
            ft.IconButton(ft.icons.SUPERVISED_USER_CIRCLE,on_click=lambda e: print('usuario logado')),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(icon=ft.icons.BRIGHTNESS_4, text='Mudar tema', on_click=mudar_tema),
                    ft.PopupMenuItem(content=ft.Text("Sair do Sistema", color=ft.colors.RED), on_click=lambda _: page.window_destroy())
                ]
            )
        ]
    )

    page.on_keyboard_event = on_enter
    page.update()

    todo = TodoApp()
    
    page.add(todo)

ft.app(target=main)