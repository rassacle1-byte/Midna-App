import flet as ft

def main(page: ft.Page):
    # Configuración de la ventana (Estilo futurista y sin bordes)
    page.title = "Midna AI"
    page.window_title_bar_hidden = True  # Oculta la barra de arriba
    page.window_title_bar_buttons_hidden = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"  # Fondo casi negro
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Recuperar el nombre guardado si existe
    nombre_guardado = page.client_storage.get("user_name")

    def guardar_nombre(e):
        if campo_nombre.value:
            # Guardar en la memoria local
            page.client_storage.set("user_name", campo_nombre.value)
            mostrar_interfaz_principal(campo_nombre.value)

    def mostrar_interfaz_principal(nombre):
        page.controls.clear()
        # Interfaz estilo Jarvis
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"BIENVENIDO, {nombre.upper()}", 
                            size=30, 
                            color="#00EAFF", 
                            weight=ft.FontWeight.BOLD),
                    ft.Text("Sistemas Midna en línea...", color="#00EAFF", italic=True),
                    ft.Divider(color="#00EAFF", thickness=1),
                    # Aquí es donde corregimos el error de la imagen
                    ft.Image(
                        src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.CONTAIN  # <--- CORRECCIÓN DEL ERROR
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                border=ft.border.all(1, "#00EAFF"),
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=20, color="#00EAFF")
            )
        )
        page.update()

    # Lógica inicial: ¿Ya te conocemos?
    if nombre_guardado:
        mostrar_interfaz_principal(nombre_guardado)
    else:
        # Si es la primera vez, pedimos el nombre
        campo_nombre = ft.TextField(
            label="Introduce tu nombre para iniciar sistema", 
            color="#00EAFF", 
            border_color="#00EAFF",
            focused_border_color="#00EAFF"
        )
        btn_iniciar = ft.ElevatedButton(
            "VINCULAR IDENTIDAD", 
            on_click=guardar_nombre,
            style=ft.ButtonStyle(color="#00EAFF", bgcolor="#1a1a1a")
        )
        page.add(campo_nombre, btn_iniciar)

ft.app(target=main)