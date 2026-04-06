import flet as ft

def main(page: ft.Page):
    # Configuraciones ultra-básicas
    page.title = "Midna AI"
    page.theme_mode = "dark"
    page.bgcolor = "#050505"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Interfaz limpia sin iconos ni funciones complejas
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("SISTEMA MIDNA ACTIVADO", 
                        size=25, 
                        color="#00EAFF", 
                        weight="bold"),
                
                ft.Divider(color="#00EAFF"),
                
                # Imagen simple
                ft.Image(
                    src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
                    width=250,
                    height=250,
                ),
                
                ft.Text("Sistemas en línea.", 
                        size=15,
                        color="#00EAFF", 
                        italic=True),
                
            ], horizontal_alignment="center"),
            padding=50,
            border=ft.border.all(2, "#00EAFF"),
            border_radius=15,
        )
    )

    page.update()

ft.app(target=main)