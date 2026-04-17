import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN BÁSICA ---
    page.title = "MIDNA"
    page.bgcolor = "#00050A"
    page.padding = 20
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Generamos un ID simple para la memoria
    id_usuario = str(uuid.uuid4())[:8]

    # --- FUNCIÓN: VOZ ---
    def hablar(texto):
        t = texto.replace("'", "").replace("\n", " ")
        page.run_javascript(f"window.speechSynthesis.speak(new SpeechSynthesisUtterance('{t}'));")

    # --- DISEÑO DEL NÚCLEO (Solo un círculo naranja, sin iconos) ---
    nucleo = ft.Container(
        width=150,
        height=150,
        bgcolor="#FF7700",
        border_radius=75,
        alignment=ft.alignment.center,
        on_click=lambda _: activar(),
        content=ft.Text("ON", color="white", weight="bold", size=30)
    )

    # --- INTERFAZ DE CHAT ---
    chat_display = ft.Text(value="SISTEMA LISTO", color="#00FFFF")
    
    caja_chat = ft.Container(
        content=ft.Column([chat_display], scroll="auto"),
        padding=15,
        bgcolor="#050F1A",
        border=ft.border.all(1, "#00FFFF"),
        border_radius=10,
        expand=True,
        visible=False
    )

    entrada = ft.TextField(
        label="Escribe aquí...",
        border_color="#00FFFF",
        visible=False,
        on_submit=lambda e: enviar(entrada.value)
    )

    # --- LÓGICA ---
    def activar():
        inicio.visible = False
        interfaz_chat.visible = True
        page.vertical_alignment = "start"
        page.update()
        hablar("Midna activada.")

    def enviar(txt):
        if not txt: return
        chat_display.value = "..."
        page.update()
        
        url = f"https://general-runtime.voiceflow.com/state/user/{id_usuario}/interact"
        headers = {"Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ"}
        payload = {"action": {"type": "text", "payload": txt}}

        try:
            r = requests.post(url, json=payload, headers=headers).json()
            respuesta = ""
            for item in r:
                if "payload" in item and "message" in item["payload"]:
                    respuesta += item["payload"]["message"] + " "
            chat_display.value = respuesta.strip()
            hablar(chat_display.value)
        except:
            chat_display.value = "Error de red."
        
        entrada.value = ""
        page.update()

    # --- PANTALLAS ---
    inicio = ft.Column([
        ft.Text("M I D N A", size=40, color="#FF7700", weight="bold"),
        ft.Container(height=20),
        nucleo,
        ft.Text("TOCA EL CÍRCULO", color="#FF7700")
    ], horizontal_alignment="center")

    interfaz_chat = ft.Column([
        ft.Text("SISTEMA HUD", size=20, color="#00FFFF"),
        caja_chat,
        entrada
    ], visible=False, expand=True)

    page.add(inicio, interfaz_chat)

    # Activación por voz simple
    page.run_javascript("""
        var r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        r.lang = 'es-ES';
        r.continuous = true;
        r.onresult = function(e) {
            var p = e.results[e.results.length - 1][0].transcript.toLowerCase();
            if(p.includes('midna')) { document.body.click(); }
        };
        r.start();
    """)

if __name__ == "__main__":
    ft.app(target=main)