import flet as ft

def main(page: ft.Page):
    # Configuración básica compatible con versiones antiguas
    page.title = "Midna AI"
    page.theme_mode = "dark"
    page.bgcolor = "#050505"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def iniciar_sistema(e):
        if campo_nombre.value:
            nombre = campo_nombre.value
            page.controls.clear()
            
            # Interfaz estilo Jarvis / Midna
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"SISTEMA ACTIVADO", size=15, color="#00EAFF"),
                        ft.Text(nombre.upper(), size=40, color="#00EAFF", weight="bold"),
                        ft.Divider(color="#00EAFF"),
                        # Imagen sin el atributo que daba error
                        ft.Image(
                            src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
                            width=250,
                            height=250,
                        ),
                        ft.Text("Midna lista para ayudar.", color="#00EAFF", italic=True),
                    ], horizontal_alignment="center"),
                    padding=30,
                    border=ft.border.all(2, "#00EAFF"),
                    border_radius=20,
                )
            )
            page.update()

    # Pantalla de inicio (Login)
    campo_nombre = ft.TextField(
        label="Identificación de Usuario", 
        border_color="#00EAFF", 
        color="#00EAFF"
    )
    
    btn_conectar = ft.ElevatedButton(
        "CONECTAR A MIDNA", 
        on_click=iniciar_sistema,
        style=ft.ButtonStyle(color="#00EAFF")
    )

    page.add(
        ft.Text("PROYECTO MIDNA", size=30, color="#00EAFF", weight="bold"),
        campo_nombre, 
        btn_conectar
    )

ft.app(target=main)