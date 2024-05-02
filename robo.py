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
                ft.dropdown.Option("Mover Mouse e Click"),
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
            height=550,
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
        if self.comands.value == 'Mover mouse' or self.comands.value == 'Mover Mouse e Click':
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
                elif conteudo[0] == 'Mover Mouse e Click':
                    pyautogui.click(int(conteudo[1]),int(conteudo[2]), duration=1)
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
    md1 = ['!', '"', '#', '$', '%', '&', "'", '(',
            ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
            'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
            'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
            'browserback', 'browserfavorites', 'browserforward', 'browserhome',
            'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
            'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
            'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
            'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
            'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
            'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
            'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
            'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
            'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
            'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
            'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
            'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
            'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
            'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
            'command', 'option', 'optionleft', 'optionright']
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def on_route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                '/',
                [
                   appbar,
                   todo
                ],
                horizontal_alignment= ft.CrossAxisAlignment.CENTER
            )
        )
        if page.route == "/Ajuda":
            page.views.append(
                ft.View(
                    "/Ajuda",
                    [
                        ft.AppBar(title=ft.Text("Ajuda"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Nomes das teclas", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                        ft.Text(md1, selectable=True),
                        ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
                    ],
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER
                )
            )
        page.update()

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

    appbar = ft.AppBar(
        title=ft.Text(value='Automação', weight=True, size=22),
        center_title=True,
        actions=[
            ft.IconButton(ft.icons.SUPERVISED_USER_CIRCLE,on_click=lambda e: print('usuario logado')),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(icon=ft.icons.BRIGHTNESS_4, text='Mudar tema', on_click=mudar_tema),
                    ft.PopupMenuItem(icon=ft.icons.HELP_CENTER, text='Ajuda', on_click=lambda _ : page.go('/Ajuda')),
                    ft.PopupMenuItem(content=ft.Text("Sair do Sistema", color=ft.colors.RED), on_click=lambda _: page.window_destroy())
                ]
            )
        ]
    )

    page.on_keyboard_event = on_enter
    todo = TodoApp()
    page.update()

    page.on_route_change = on_route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    page.update()

ft.app(target=main)