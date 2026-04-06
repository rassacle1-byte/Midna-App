import flet as ft

def main(page: ft.Page):
    # Configuración básica (Compatible con versiones antiguas)
    page.title = "Midna AI"
    page.theme_mode = "dark"
    page.bgcolor = "#050505"  # Fondo negro tipo Jarvis
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Interfaz Principal Directa (Sin pedir nombres)
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("SISTEMA MIDNA ACTIVADO", 
                        size=20, 
                        color="#00EAFF", 
                        weight="bold"),
                
                ft.Divider(color="#00EAFF", thickness=2),
                
                # Imagen con método de carga simple
                ft.Image(
                    src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
                    width=250,
                    height=250,
                ),
                
                ft.Text("En línea y lista para procesar comandos.", 
                        color="#00EAFF", 
                        italic=True),
                
                # Un icono de envío básico
                ft.Icon(name="send", color="#00EAFF", size=30),
                
            ], horizontal_alignment="center"),
            padding=40,
            border=ft.border.all(2, "#00EAFF"),
            border_radius=20,
        )
    )

    page.update()

# Ejecutar la aplicación
ft.app(target=main)