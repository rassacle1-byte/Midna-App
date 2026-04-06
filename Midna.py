import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS PROTOCOL ---
    page.title = "MIDNA - JARVIS Protocol"
    page.theme_mode = ft.ThemeMode.DARK
    # Fondo gris muy oscuro, casi negro, para que resalte el neón
    page.bgcolor = "#05070A" 
    page.padding = 30
    # Un poco más ancha para que se vea más imponente en PC
    page.window_width = 500 
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- DEFINICIÓN DE COLORES STARK INDUSTRIES ---
    NEON_CYAN = "#00FFFF" # Azul cian neón principal
    DARK_BLUE = "#001F3F" # Azul oscuro para fondos de contenedores
    GLOW_EFFECT = "0 0 10px #00FFFF" # Efecto de brillo para sombras

    # --- ELEMENTOS DE LA INTERFAZ ---
    # Texto de bienvenida que cambiará según la memoria
    label_respuesta = ft.Text(
        value="A LA ESPERA DE IDENTIFICACIÓN... PROTOCOLO MIDNA INICIADO.", 
        size=16, 
        color=NEON_CYAN,
        font_family="Consolas", # Fuente tipo código/terminal
    )

    # Contenedor con scroll para respuestas largas, con borde neón
    contenedor_chat = ft.Container(
        content=ft.Column(
            controls=[label_respuesta],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=20,
        bgcolor="#0A111A", # Fondo de contenedor muy oscuro
        border=ft.border.all(2, NEON_CYAN), # Borde cian neón
        border_radius=5, # Esquinas poco redondeadas
        expand=True,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN), # Efecto de brillo exterior
    )

    # Campo de mensaje con estilo tecnológico
    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", 
        border_color=NEON_CYAN,
        border_radius=5,
        color=NEON_CYAN,
        label_style=ft.TextStyle(color=NEON_CYAN, font_family="Consolas"),
        cursor_color=NEON_CYAN,
        on_submit=lambda e: enviar_a_midna(e),
        width=450,
    )

    # Campo de nombre con estilo tecnológico y color de resalte
    input_nombre = ft.TextField(
        label="IDENTIFICACIÓN REQUERIDA",
        width=300,
        border_color="#FACC15", # Color amarillo/dorado Stark para el nombre
        color="#FACC15",
        label_style=ft.TextStyle(color="#FACC15", font_family="Consolas"),
        hint_text="Escribe tu nombre...",
        hint_style=ft.TextStyle(color="#FACC15"),
    )

    # Fila que contiene el campo de nombre para ocultarla
    fila_identificacion = ft.Row(
        controls=[input_nombre],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=True 
    )

    # --- FUNCIÓN DE ENVÍO DE DATOS ---
    def enviar_a_midna(e):
        # LÓGICA DE MEMORIA (Mantenemos la que creamos)
        if not page.client_storage.contains("midna_user_id"):
            if not input_nombre.value:
                label_respuesta.value = "❌ ERROR: IDENTIFICACIÓN REQUERIDA. INGRESE NOMBRE."
                label_respuesta.color = "#FF4444" # Rojo para error
                page.update()
                return
            # Guardar el nombre en el celular/navegador
            page.client_storage.set("midna_user_id", input_nombre.value)
            fila_identificacion.visible = False
            label_respuesta.color = NEON_CYAN # Restaurar color cian

        if not input_mensaje.value:
            return

        # Recuperar el nombre guardado para la sesión
        usuario_actual = page.client_storage.get("midna_user_id")
        comando_texto = input_mensaje.value
        
        label_respuesta.value = f"PROCESANDO COMANDO DE {usuario_actual.upper()}..."
        page.update()

        # CONEXIÓN CON VOICEFLOW
        url_api = f"https://general-runtime.voiceflow.com/state/user/{usuario_actual}/interact"
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        # Enviamos el mensaje indicando quién habla
        payload = {
            "action": {"type": "text", "payload": f"Soy {usuario_actual}. {comando_texto}"}
        }

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            mensaje_final = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            label_respuesta.value = mensaje_final.strip()
        except:
            label_respuesta.value = "❌ ERROR DE CONEXIÓN CON EL NÚCLEO CENTRAL."
            label_respuesta.color = "#FF4444"
        
        input_mensaje.value = ""
        page.update()

    # --- LÓGICA DE MEMORIA AL INICIAR ---
    if page.client_storage.contains("midna_user_id"):
        usuario_registrado = page.client_storage.get("midna_user_id")
        fila_identificacion.visible = False # Ocultar si ya lo conocemos
        label_respuesta.value = f"SISTEMA ONLINE. BIENVENIDO DE NUEVO, {usuario_registrado.upper()}."

    # --- DISEÑO FINAL DE LA PANTALLA ---
    page.add(
        # Encabezado con estilo Stark
        ft.Row(
            controls=[
                ft.Text("M I D N A", size=40, weight="bold", color=NEON_CYAN, font_family="Consolas"),
                ft.Text("SYSTEMS", size=18, color=NEON_CYAN, font_family="Consolas"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Divider(height=10, color="transparent"),
        
        # Estado del protocolo
        ft.Text("STATUS: ONLINE", size=12, color="#00FF00", font_family="Consolas"), # Verde para online
        ft.Divider(height=20, color="transparent"),

        # Fila de identificación (desaparecerá)
        fila_identificacion,
        
        # El núcleo del chat futurista
        contenedor_chat,
        
        ft.Divider(height=20, color="transparent"),
        
        # Input y Botón de envío
        ft.Row(
            controls=[
                input_mensaje,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Container(height=15),
        ft.ElevatedButton(
            "ENVIAR COMANDO", 
            on_click=enviar_a_midna, 
            bgcolor=DARK_BLUE, 
            color=NEON_CYAN,
            width=200,
            height=50,
            # Pequeña sombra cian en el botón
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=NEON_CYAN), 
        ),
        # Pie de página Stark Industries
        ft.Container(height=20),
        ft.Text("© STARK INDUSTRIES - MALIBU POINT", size=10, color="gray", font_family="Consolas"),
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)