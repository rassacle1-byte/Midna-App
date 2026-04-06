import flet as ft

def main(page: ft.Page):
    page.title = "Midna AI Interface"
    page.theme_mode = "dark"
    page.bgcolor = "#050505"
    page.padding = 20
    
    # Historial de Chat con Scroll para textos largos
    historial_chat = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        spacing=15,
    )

    def enviar_mensaje(e):
        if campo_entrada.value:
            # Tu mensaje
            historial_chat.controls.append(
                ft.Container(
                    content=ft.Text(campo_entrada.value, color="white"),
                    padding=12,
                    bgcolor="#1a1a1a",
                    border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                    alignment=ft.alignment.center_right,
                )
            )
            # Respuesta visual de Midna
            historial_chat.controls.append(
                ft.Container(
                    content=ft.Text("Procesando comando...", color="#00EAFF", italic=True),
                    padding=12,
                    border=ft.border.all(1, "#00EAFF"),
                    border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15),
                )
            )
            campo_entrada.value = ""
            page.update()

    # Cuadro de texto MULTILÍNEA (Ideal para textos largos)
    campo_entrada = ft.TextField(
        hint_text="Escribe a Midna...",
        multiline=True,
        min_lines=1,
        max_lines=4,
        expand=True,
        border_color="#00EAFF",
        focused_border_color="#00EAFF",
        color="#00EAFF",
        text_size=16,
    )

    # BOTÓN DE ENVIAR (Icono estilo futurista)
    btn_enviar = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            icon_color="#050505",
            on_click=enviar_mensaje,
        ),
        bgcolor="#00EAFF",
        border_radius=10,
        margin=ft.margin.only(left=10)
    )

    # Estructura Principal
    page.add(
        ft.Text("MIDNA CORE v1.0", size=12, color="#00EAFF", weight="bold", opacity=0.6),
        
        # Área de mensajes con borde de neón
        ft.Container(
            content=historial_chat,
            expand=True,
            padding=15,
            border=ft.border.all(1, "#1a1a1a"),
            border_radius=15,
            bgcolor="#0a0a0a",
        ),
        
        # Barra inferior de entrada
        ft.Row(
            controls=[
                campo_entrada,
                btn_enviar
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.END
        )
    )

ft.app(target=main)