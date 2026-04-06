import flet as ft

def main(page: ft.Page):
    page.title = "Midna AI"
    page.bgcolor = "#050505"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "always" # Permite bajar si el texto es muy largo

    # Función para cuando presionas el botón
    def enviar_mensaje(e):
        if campo_texto.value:
            # Aquí Midna procesaría el texto
            print(f"Enviando a Midna: {campo_texto.value}")
            campo_texto.value = "" # Limpia el cuadro después de enviar
            page.update()

    # Cuadro para escribir (Multilínea para textos largos)
    campo_texto = ft.TextField(
        label="Escribe aquí...",
        color="#00EAFF",
        border_color="#00EAFF",
        multiline=True,       # <--- Esto permite que el texto sea largo
        min_lines=1,
        max_lines=5,          # Crece hasta 5 líneas antes de poner scroll interno
    )

    # Botón de enviar (Versión ultra-compatible)
    btn_enviar = ft.ElevatedButton(
        text="ENVIAR COMANDO",
        on_click=enviar_mensaje,
        color="#00EAFF",
    )

    # Contenedor principal de la interfaz
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("INTERFAZ MIDNA", size=25, color="#00EAFF", weight="bold"),
                    ft.Divider(color="#00EAFF"),
                    
                    # Espacio para la imagen/logo
                    ft.Image(
                        src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
                        width=150,
                        height=150,
                    ),
                    
                    # Sección de entrada de usuario
                    ft.Text("ENTRADA DE DATOS:", color="#00EAFF", size=12),
                    campo_texto,
                    btn_enviar,
                    
                    ft.Text("Sistemas Midna v1.0 - Esperando...", color="#00EAFF", size=10, italic=True),
                ],
                horizontal_alignment="center",
            ),
            padding=30,
            border=ft.border.all(2, "#00EAFF"),
            border_radius=15,
            width=400, # Ancho fijo para que se vea como una app de escritorio
        )
    )

    page.update()

ft.app(target=main)