import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS ---
    page.title = "MIDNA - JARVIS Protocol"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#05070A" 
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    NEON_CYAN = "#00FFFF"
    DARK_BLUE = "#001F3F"

    # --- ELEMENTOS ---
    label_respuesta = ft.Text(
        value="A LA ESPERA DE IDENTIFICACIÓN...", 
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
        bgcolor="#0A111A",
        border=ft.border.all(2, NEON_CYAN),
        border_radius=5,
        expand=True,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN),
    )

    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", 
        border_color=NEON_CYAN,
        color=NEON_CYAN,
        on_submit=lambda e: enviar_a_midna(e),
    )

    input_nombre = ft.TextField(
        label="IDENTIFICACIÓN REQUERIDA",
        border_color="#FACC15",
        color="#FACC15",
        hint_text="Tu nombre..."
    )

    fila_identificacion = ft.Row(
        controls=[input_nombre],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def enviar_a_midna(e):
        # Si la barra de nombre es visible, significa que es el primer mensaje
        if fila_identificacion.visible:
            if not input_nombre.value:
                label_respuesta.value = "❌ ERROR: IDENTIFICACIÓN REQUERIDA."
                page.update()
                return
            
            # Ocultamos la barra de nombre y seguimos
            fila_identificacion.visible = False
            page.update()

        if not input_mensaje.value:
            return

        nombre_usuario = input_nombre.value
        comando_texto = input_mensaje.value
        
        label_respuesta.value = f"PROCESANDO COMANDO DE {nombre_usuario.upper()}..."
        page.update()

        url_api = f"https://general-runtime.voiceflow.com/state/user/{nombre_usuario}/interact"
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        payload = {"action": {"type": "text", "payload": f"Soy {nombre_usuario}. {comando_texto}"}}

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            mensaje_final = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            label_respuesta.value = mensaje_final.strip()
        except:
            label_respuesta.value = "❌ ERROR DE ENLACE CON EL NÚCLEO."
        
        input_mensaje.value = ""
        page.update()

    # --- DISEÑO FINAL ---
    page.add(
        ft.Text("M I D N A", size=40, weight="bold", color=NEON_CYAN, font_family="Consolas"),
        fila_identificacion,
        contenedor_chat,
        ft.Container(height=10),
        input_mensaje,
        ft.ElevatedButton(
            "EJECUTAR", 
            on_click=enviar_a_midna, 
            bgcolor=DARK_BLUE, 
            color=NEON_CYAN
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)
