import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS ---
    page.title = "MIDNA - PURE CODE"
    page.theme_mode = "dark" 
    page.bgcolor = "#00050A"
    page.padding = 0
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    id_acceso = str(uuid.uuid4())[:8].upper()
    NEON_CYAN = "#00FFFF"
    NEON_ORANGE = "#FF7700"

    # --- FUNCIÓN: VOZ DE MIDNA ---
    def midna_habla(texto):
        texto_limpio = texto.replace("'", "").replace("\n", " ")
        page.run_javascript(f"window.speechSynthesis.speak(new SpeechSynthesisUtterance('{texto_limpio}'));")

    # --- DISEÑO DEL NÚCLEO (HECHO 100% CON CÓDIGO) ---
    nucleo_dibujo = ft.Stack([
        # Anillo exterior tenue
        ft.Container(width=220, height=220, border_radius=110, border=ft.border.all(1, "#331100")),
        # Anillo medio
        ft.Container(width=180, height=180, border_radius=90, border=ft.border.all(2, NEON_ORANGE)),
        # Centro brillante
        ft.Container(
            width=120, height=120, border_radius=60, 
            bgcolor="#442200",
            content=ft.Icon(name="power_settings_new", color=NEON_ORANGE, size=50)
        )
    ], alignment=ft.alignment.center)

    # --- INTERFAZ DE CHAT AZUL (HUD) ---
    label_respuesta = ft.Text(value="SISTEMA ONLINE...", size=16, color=NEON_CYAN, font_family="Consolas")
    
    contenedor_chat = ft.Container(
        content=ft.Column([label_respuesta], scroll="auto", expand=True),
        padding=20, 
        bgcolor="#050F1A", # Fondo azul oscuro sólido
        border=ft.border.all(2, NEON_CYAN),
        border_radius=10, 
        expand=True, 
        visible=False
    )

    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", 
        border_color=NEON_CYAN, 
        color=NEON_CYAN,
        visible=False, 
        on_submit=lambda e: enviar_a_midna(input_mensaje.value)
    )

    # --- LÓGICA DE ACTIVACIÓN ---
    def activar_protocolo(e):
        pantalla_inicio.visible = False
        pantalla_chat.visible = True
        page.vertical_alignment = "start"
        page.update()
        midna_habla("Protocolo Midna iniciado. ¿Qué órdenes tiene para hoy, Leo?")

    # --- PANTALLA DE INICIO (Naranja) ---
    pantalla_inicio = ft.Container(
        content=ft.Column([
            ft.Text("M I D N A", size=50, weight="bold", color=NEON_ORANGE),
            ft.Container(height=30),
            ft.GestureDetector(content=nucleo_dibujo, on_tap=activar_protocolo),
            ft.Container(height=30),
            ft.Text("TOCA EL NÚCLEO O DI 'MIDNA'", color=NEON_ORANGE, size=14, weight="bold")
        ], horizontal_alignment="center"),
        expand=True
    )

    # --- PANTALLA DE CHAT (Azul) ---
    pantalla_chat = ft.Container(
        content=ft.Column([
            ft.Text("M I D N A   H U D", size=30, weight="bold", color=NEON_CYAN),
            contenedor_chat,
            ft.Container(height=10),
            input_mensaje,
            ft.Text("SISTEMA DE VOZ ACTIVO", color=NEON_CYAN, size=10)
        ]),
        visible=False, expand=True, padding=20
    )

    # --- CONEXIÓN CON VOICEFLOW ---
    def enviar_a_midna(texto):
        if not texto: return
        label_respuesta.value = "TRANSMITIENDO..."
        page.update()
        
        url = f"https://general-runtime.voiceflow.com/state/user/{id_acceso}/interact"
        headers = {"Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ"}
        payload = {"action": {"type": "text", "payload": texto}}

        try:
            res = requests.post(url, json=payload, headers=headers).json()
            msg = ""
            for item in res:
                if item.get("type") in ["text", "speak"]:
                    msg += item["payload"]["message"] + " "
            label_respuesta.value = msg.strip()
            midna_habla(label_respuesta.value)
        except:
            label_respuesta.value = "ERROR: NÚCLEO NO RESPONDE."
        
        input_mensaje.value = ""
        page.update()

    # --- RECONOCIMIENTO DE VOZ (JS) ---
    def iniciar_microfono():
        page.run_javascript("""
            const Reco = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            Reco.lang = 'es-ES';
            Reco.continuous = true;
            Reco.onresult = (e) => {
                const p = e.results[e.results.length - 1][0].transcript.toLowerCase();
                if (p.includes('midna')) {
                    // Simula un click para activar la interfaz
                    document.body.click(); 
                }
            };
            Reco.start();
        """)

    # --- AÑADIR TODO A LA PÁGINA ---
    page.add(ft.Stack([pantalla_inicio, pantalla_chat], expand=True))
    iniciar_microfono()

if __name__ == "__main__":
    ft.app(target=main, view="web_browser", port=8080)