import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS 3.0 (SIN SESIONES) ---
    page.title = "MIDNA - JARVIS Protocol"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Generamos un ID de acceso rápido para la sesión actual
    id_acceso = str(uuid.uuid4())[:8].upper()

    NEON_CYAN = "#00FFFF"
    DARK_BLUE = "#001F3FEE"

    # --- ELEMENTOS ---
    label_respuesta = ft.Text(
        value=f"SISTEMA ONLINE.\nID: {id_acceso}\nESPERANDO COMANDO...", 
        size=16, 
        color=NEON_CYAN,
        font_family="Consolas"
    )

    contenedor_chat = ft.Container(
        content=ft.Column(
            controls=[label_respuesta],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=20,
        bgcolor="#0A111AEE",
        border=ft.border.all(2, NEON_CYAN),
        border_radius=5,
        expand=True,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN),
    )

    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", 
        border_color=NEON_CYAN,
        color=NEON_CYAN,
        bgcolor="#05070AEE",
        on_submit=lambda e: enviar_a_midna(e),
    )

    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        comando = input_mensaje.value
        label_respuesta.value = "TRANSMITIENDO..."
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
            label_respuesta.value = "❌ ERROR: FALLO EN EL NÚCLEO."
        
        input_mensaje.value = ""
        page.update()

    # --- LÓGICA DE FONDO ---
    # REEMPLAZA EL NOMBRE ENTRE COMILLAS CON TU USUARIO DE GITHUB
    mi_usuario = "rassacle1-byte" 
    fondo_url = f"https://raw.githubusercontent.com/{mi_usuario}/Midna-App/main/fondo_hud.png"

    layout = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("M I D N A", size=45, weight="bold", color=NEON_CYAN),
                ft.Text("JARVIS PROTOCOL", size=14, color=NEON_CYAN),
                ft.Divider(height=10, color="transparent"),
                contenedor_chat,
                ft.Divider(height=10, color="transparent"),
                input_mensaje,
                ft.ElevatedButton(
                    "EJECUTAR", 
                    on_click=enviar_a_midna, 
                    bgcolor=DARK_BLUE, 
                    color=NEON_CYAN,
                    width=200
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=20,
        image_src=fondo_url,
        image_fit=ft.ImageFit.COVER,
        expand=True,
    )

    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)