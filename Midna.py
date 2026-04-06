import flet as ft
import time

def main(page: ft.Page):
    # 1. CONFIGURACIÓN FUTURISTA (Ahora sí funcionará)
    page.title = "Midna AI"
    page.window_title_bar_hidden = True  # Sin barra de arriba
    page.window_title_bar_buttons_hidden = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.window_resizable = True
    page.window_width = 450
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 2. MEMORIA: Intentar recuperar el nombre guardado
    nombre_guardado = page.client_storage.get("user_name")

    def guardar_nombre(e):
        if campo_nombre.value:
            # Guardamos el nombre "para siempre" en la PC
            page.client_storage.set("user_name", campo_nombre.value)
            iniciar_animacion_sistema(campo_nombre.value)

    def iniciar_animacion_sistema(nombre):
        page.controls.clear()
        # Efecto de carga tipo Jarvis
        progreso = ft.ProgressBar(width=300, color="#00EAFF", bgcolor="#1a1a1a")
        texto_carga = ft.Text("Sincronizando redes neuronales...", color="#00EAFF", italic=True)
        
        page.add(
            ft.Column([
                ft.Text("INICIANDO MIDNA", size=20, color="#00EAFF", weight="bold"),
                progreso,
                texto_carga
            ], horizontal_alignment="center")
        )
        page.update()
        
        time.sleep(1.5) # Pausa dramática para el efecto
        mostrar_interfaz_principal(nombre)

    def mostrar_interfaz_principal(nombre):
        page.controls.clear()
        
        # Interfaz Principal Estilo "Glow"
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.STAIRS_OUTLINED, color="#00EAFF"),
                        ft.Text("SISTEMA MIDNA V3.0", size=12, color="#00EAFF", weight="bold"),
                    ], alignment="center"),
                    
                    ft.Divider(color="#00EAFF", height=30),
                    
                    ft.Text(f"HOLA, {nombre.upper()}", size=35, color="#00EAFF", weight="bold"),
                    
                    # Imagen con el atributo corregido
                    ft.Image(
                        src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
                        width=250,
                        height=250,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    
                    ft.Text("Estado: En línea y lista.", color="#00EAFF", italic=True),
                    
                    ft.IconButton(
                        icon=ft.icons.SEND_ROUNDED, # Este es el que antes daba error
                        icon_color="#00EAFF",
                        icon_size=40,
                        tooltip="Enviar comando de voz"
                    ),
                ], horizontal_alignment="center"),
                padding=40,
                border=ft.border.all(1, "#00EAFF"),
                border_radius=30,
                shadow=ft.BoxShadow(blur_radius=30, color="#00EAFF", spread_radius=-10)
            )
        )
        page.update()

    # Lógica de inicio: Si ya te conoce, entra directo
    if nombre_guardado:
        mostrar_interfaz_principal(nombre_guardado)
    else:
        # Pantalla de vinculación inicial
        campo_nombre = ft.TextField(
            label="Identificación de Usuario", 
            border_color="#00EAFF", 
            focused_border_color="#00EAFF",
            color="#00EAFF",
            width=300,
            text_align="center"
        )
        
        btn_conectar = ft.ElevatedButton(
            text="VINCULAR IDENTIDAD", 
            on_click=guardar_nombre,
            style=ft.ButtonStyle(
                color="#00EAFF",
                bgcolor="#1a1a1a",
                side={"": ft.BorderSide(1, "#00EAFF")}
            )
        )

        page.add(
            ft.Icon(ft.icons.FINGERPRINT, color="#00EAFF", size=80),
            ft.Text("ACCESO RESTRINGIDO", size=25, color="#00EAFF", weight="bold"),
            ft.Container(height=20),
            campo_nombre, 
            btn_conectar
        )

ft.app(target=main)