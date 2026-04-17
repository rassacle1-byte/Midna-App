import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS ---
    page.title = "MIDNA - CORE ENGINE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#00050A"
    page.padding = 0
    page.margin = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    id_acceso = str(uuid.uuid4())[:8].upper()
    NEON_CYAN = "#00FFFF"
    NEON_ORANGE = "#FF7700"

    # --- FUNCIÓN: VOZ ---
    def midna_habla(texto):
        texto_limpio = texto.replace("'", "").replace("\n", " ")
        page.run_javascript(f"window.speechSynthesis.speak(new SpeechSynthesisUtterance('{texto_limpio}'));")

    # --- DIBUJO DEL NÚCLEO (CÓDIGO PURO) ---
    nucleo_dibujo = ft.Stack([
        ft.Container(width=250, height=250, border_radius=125, border=ft.border.all(1, NEON_ORANGE), opacity=0.2),
        ft.Container(width=200, height=200, border_radius=100, border=ft.border.all(3, NEON_ORANGE), opacity=0.4),
        ft.Container(
            width=150, height=150, border_radius=75, 
            bgcolor=ft.colors.with_opacity(0.1, NEON_ORANGE),
            border=ft.border.all(8, NEON_ORANGE),
            shadow=ft.BoxShadow(spread_radius=10, blur_radius=40, color=NEON_ORANGE)
        ),
        ft.Icon(name=ft.icons.POWER_SETTINGS_NEW, color=NEON_ORANGE, size=60)
    ], alignment=ft.alignment.center)

    # --- INTERFAZ DE CHAT (OCULTA AL INICIO) ---
    label_respuesta = ft.Text(value="SISTEMA ONLINE...", size=16, color=NEON_CYAN, font_family="Consolas")
    
    contenedor_chat = ft.Container(
        content=ft.Column([label_respuesta], scroll=ft.ScrollMode.AUTO, expand=True),
        padding=20, bgcolor="#050F1AEE", border=ft.border.all(1, NEON_CYAN),
        border_radius=10, expand=True, visible=False,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=NEON_CYAN)
    )

    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", border_color=NEON_CYAN, color=NEON_CYAN,
        visible=False, on_submit=lambda e: enviar_a_midna(input_mensaje.value)
    )

    # --- LÓGICA DE CAMBIO DE INTERFAZ ---
    def activar_midna(e=None):
        pantalla_inicio.visible = False
        pantalla_chat.visible = True
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.update()
        midna_habla("Protocolo Midna iniciado. Sistemas al cien por ciento.")

    # --- PANTALLAS ---
    pantalla_inicio = ft.Container(
        content=ft.Column([
            ft.Text("M I D N A", size=50, weight="bold", color=NEON_ORANGE, font_family="Consolas"),
            ft.Container(height=40),
            ft.GestureDetector(content=nucleo_dibujo, on_tap=activar_protocolo),
            ft.Container(height=40),
            ft.Text("DI 'MIDNA' O TOCA EL NÚCLEO", color=NEON_ORANGE, size=16, italic=True)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True, alignment=ft.alignment.center
    )

    pantalla_chat = ft.Container(
        content=ft.Column([
            ft.Text("M I D N A   H U D", size=30, weight="bold", color=NEON_CYAN),
            contenedor_chat,
            ft.Container(height=10),
            input_mensaje,
            ft.IconButton(icon=ft.icons.MIC, icon_color=NEON_CYAN, icon_size=30, on_click=lambda _: None)
        ]),
        visible=False, expand=True, padding=30
    )

    def activar_protocolo(e=None):
        activar_midna()

    # --- COMUNICACIÓN ---
    def enviar_a_midna(texto):
        if not texto: return
        label_respuesta.value = "PROCESANDO..."
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
            label_respuesta.value = "ERROR DE ENLACE."
        input_mensaje.value = ""
        page.update()

    # --- VOZ (JS) ---
    def iniciar_microfono():
        page.run_javascript("""
            const Reco = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            Reco.lang = 'es-ES';
            Reco.continuous = true;
            Reco.onresult = (e) => {
                const p = e.results[e.results.length - 1][0].transcript.toLowerCase();
                if (p.includes('midna')) document.dispatchEvent(new CustomEvent('activar_m'));
            };
            Reco.start();
        """)

    # --- CARGA FINAL ---
    page.add(ft.Stack([pantalla_inicio, pantalla_chat]))
    iniciar_microfono()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)