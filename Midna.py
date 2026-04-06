import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS ESTABLE ---
    page.title = "MIDNA - JARVIS Protocol"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ID de sesión simple
    id_acceso = str(uuid.uuid4())[:8].upper()

    NEON_CYAN = "#00FFFF"
    DARK_BLUE = "#001F3F"

    # --- ELEMENTOS ---
    label_respuesta = ft.Text(
        value=f"SISTEMA ONLINE. ID: {id_acceso}", 
        size=16, 
        color=NEON_CYAN,
        font_family="Consolas"
    )

    # Caja de chat con scroll
    contenedor_chat = ft.Container(
        content=ft.Column(
            controls=[label_respuesta],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=20,
        bgcolor="#0A111A", # Fondo oscuro sólido para evitar errores de transparencia
        border=ft.border.all(2, NEON_CYAN),
        border_radius=5,
        expand=True,
    )

    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", 
        border_color=NEON_CYAN,
        color=NEON_CYAN,
        on_submit=lambda e: enviar_a_midna(e),
    )

    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        comando = input_mensaje.value
        label_respuesta.value = "PROCESANDO..."
        page.update()

        url_api = f"https://general-runtime.voiceflow.com/state/user/{id_acceso}/interact"
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        payload = {"action": {"type": "text", "payload": comando}}

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            mensaje_final = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            label_respuesta.value = mensaje_final.strip()
        except:
            label_respuesta.value = "❌ ERROR DE CONEXIÓN."
        
        input_mensaje.value = ""
        page.update()

    # --- FONDO SIMPLIFICADO ---
    # Reemplaza 'tu_usuario' por tu usuario real de GitHub
    mi_usuario = "rassacle1-byte" 
    
    # He quitado 'ImageFit' para que no de error
    page.add(
        ft.Stack([
            # Imagen de fondo simple
            ft.Image(
                src=f"https://raw.githubusercontent.com/{mi_usuario}/Midna-App/main/fondo_hud.png",
                opacity=0.3, # La hacemos un poco transparente para que se vea el chat
            ),
            # Contenido principal
            ft.Column([
                ft.Text("M I D N A", size=40, weight="bold", color=NEON_CYAN),
                contenedor_chat,
                ft.Container(height=10),
                input_mensaje,
                ft.ElevatedButton(
                    "EJECUTAR", 
                    on_click=enviar_a_midna, 
                    bgcolor=DARK_BLUE, 
                    color=NEON_CYAN,
                    width=200
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)