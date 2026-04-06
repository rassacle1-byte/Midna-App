import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS ---
    page.title = "MIDNA - JARVIS Protocol"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#05070A" 
    page.padding = 30
    page.window_width = 450
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    NEON_CYAN = "#00FFFF"
    DARK_BLUE = "#001F3F"

    # --- ELEMENTOS ---
    label_respuesta = ft.Text(
        value="INICIALIZANDO SISTEMA...", 
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
    )

    fila_identificacion = ft.Row(
        controls=[input_nombre],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=True 
    )

    # --- LÓGICA CORREGIDA ---
    def enviar_a_midna(e):
        # Usamos page.session para evitar el error de 'client_storage'
        nombre_en_memoria = page.session.get("nombre")

        if not nombre_en_memoria:
            if not input_nombre.value:
                label_respuesta.value = "❌ ERROR: IDENTIFICACIÓN REQUERIDA."
                page.update()
                return
            
            page.session.set("nombre", input_nombre.value)
            fila_identificacion.visible = False
            nombre_en_memoria = input_nombre.value

        if not input_mensaje.value:
            return

        comando_texto = input_mensaje.value
        label_respuesta.value = f"PROCESANDO COMANDO DE {nombre_en_memoria.upper()}..."
        page.update()

        url_api = f"https://general-runtime.voiceflow.com/state/user/{nombre_en_memoria}/interact"
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        payload = {"action": {"type": "text", "payload": f"Soy {nombre_en_memoria}. {comando_texto}"}}

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

    # --- CHEQUEO INICIAL ---
    # Si la sesión ya tiene nombre, ocultamos la barra
    if page.session.get("nombre"):
        fila_identificacion.visible = False
        label_respuesta.value = f"SISTEMA ONLINE. BIENVENIDO, {page.session.get('nombre').upper()}."
    else:
        label_respuesta.value = "A LA ESPERA DE IDENTIFICACIÓN..."

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
    # Importante mantener el puerto 8080 para Render
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS ---
    page.title = "MIDNA - JARVIS Protocol"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#05070A" 
    page.padding = 30
    page.window_width = 450
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    NEON_CYAN = "#00FFFF"
    DARK_BLUE = "#001F3F"

    # --- ELEMENTOS ---
    label_respuesta = ft.Text(
        value="INICIALIZANDO SISTEMA...", 
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
    )

    fila_identificacion = ft.Row(
        controls=[input_nombre],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=True 
    )

    # --- LÓGICA CORREGIDA ---
    def enviar_a_midna(e):
        # Usamos page.session para evitar el error de 'client_storage'
        nombre_en_memoria = page.session.get("nombre")

        if not nombre_en_memoria:
            if not input_nombre.value:
                label_respuesta.value = "❌ ERROR: IDENTIFICACIÓN REQUERIDA."
                page.update()
                return
            
            page.session.set("nombre", input_nombre.value)
            fila_identificacion.visible = False
            nombre_en_memoria = input_nombre.value

        if not input_mensaje.value:
            return

        comando_texto = input_mensaje.value
        label_respuesta.value = f"PROCESANDO COMANDO DE {nombre_en_memoria.upper()}..."
        page.update()

        url_api = f"https://general-runtime.voiceflow.com/state/user/{nombre_en_memoria}/interact"
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        payload = {"action": {"type": "text", "payload": f"Soy {nombre_en_memoria}. {comando_texto}"}}

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

    # --- CHEQUEO INICIAL ---
    # Si la sesión ya tiene nombre, ocultamos la barra
    if page.session.get("nombre"):
        fila_identificacion.visible = False
        label_respuesta.value = f"SISTEMA ONLINE. BIENVENIDO, {page.session.get('nombre').upper()}."
    else:
        label_respuesta.value = "A LA ESPERA DE IDENTIFICACIÓN..."

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
    # Importante mantener el puerto 8080 para Render
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)