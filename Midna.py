import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS ---
    page.title = "MIDNA - PROTOCOLO PERSISTENCIA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#05070A" 
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    NEON_CYAN = "#00FFFF"
    DARK_BLUE = "#001F3F"

    # --- ELEMENTOS ---
    label_respuesta = ft.Text(
        value="SISTEMA INICIALIZADO...", 
        size=16, 
        color=NEON_CYAN,
        font_family="Consolas"
    )

    contenedor_chat = ft.Container(
        content=ft.Column(controls=[label_respuesta], scroll=ft.ScrollMode.AUTO, expand=True),
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
    )

    fila_identificacion = ft.Row(
        controls=[input_nombre],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # --- LÓGICA DE PERSISTENCIA REAL ---
    def enviar_a_midna(e):
        # Intentamos recuperar del almacenamiento local del cliente
        nombre_guardado = page.client_storage.get("usuario_registrado")

        if not nombre_guardado:
            if not input_nombre.value:
                label_respuesta.value = "❌ ERROR: IDENTIFICACIÓN REQUERIDA."
                page.update()
                return
            
            # GUARDAR DE FORMA PERSISTENTE
            nombre_guardado = input_nombre.value
            page.client_storage.set("usuario_registrado", nombre_guardado)
            fila_identificacion.visible = False
            label_respuesta.value = f"IDENTIDAD CONFIRMADA: {nombre_guardado.upper()}"
            page.update()

        if not input_mensaje.value:
            return

        comando = input_mensaje.value
        label_respuesta.value = f"PROCESANDO COMANDO DE {nombre_guardado.upper()}..."
        page.update()

        # Enlace con Voiceflow
        url_api = f"https://general-runtime.voiceflow.com/state/user/{nombre_guardado}/interact"
        headers = {"Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", "Content-Type": "application/json"}
        payload = {"action": {"type": "text", "payload": f"Soy {nombre_guardado}. {comando}"}}

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            res = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    res += item["payload"]["message"] + "\n\n"
            label_respuesta.value = res.strip()
        except:
            label_respuesta.value = "❌ ERROR DE ENLACE."
        
        input_mensaje.value = ""
        page.update()

    # --- REVISIÓN AL CARGAR LA PÁGINA ---
    # Esto corre apenas abres la app
    def revisar_login():
        user = page.client_storage.get("usuario_registrado")
        if user:
            fila_identificacion.visible = False
            label_respuesta.value = f"ACCESO CONCEDIDO. BIENVENIDO DE NUEVO, {user.upper()}."
            page.update()

    # --- DISEÑO ---
    page.add(
        ft.Text("M I D N A", size=40, weight="bold", color=NEON_CYAN, font_family="Consolas"),
        fila_identificacion,
        contenedor_chat,
        ft.Container(height=10),
        input_mensaje,
        ft.ElevatedButton("EJECUTAR", on_click=enviar_a_midna, bgcolor=DARK_BLUE, color=NEON_CYAN)
    )

    # Ejecutamos la revisión de memoria al entrar
    revisar_login()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)