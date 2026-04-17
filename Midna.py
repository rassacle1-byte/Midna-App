import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN TOTALMENTE COMPATIBLE ---
    page.title = "MIDNA"
    page.bgcolor = "#00050A"
    page.padding = 20
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # ID para que Voiceflow te reconozca y tenga memoria
    id_usuario = str(uuid.uuid4())[:8]

    # --- FUNCIÓN: VOZ ---
    def hablar(texto):
        t = texto.replace("'", "").replace("\n", " ")
        page.run_javascript("window.speechSynthesis.speak(new SpeechSynthesisUtterance('" + t + "'));")

    # --- DISEÑO DEL NÚCLEO (Sin nombres de iconos que fallen) ---
    nucleo = ft.Container(
        content=ft.Icon(ft.icons.PLAY_CIRCLE_FILL, color="#FF7700", size=80),
        width=200,
        height=200,
        bgcolor="#1A0D00",
        border_radius=100,
        border=ft.border.all(4, "#FF7700"),
        alignment=ft.alignment.center,
        on_click=lambda _: activar()
    )

    # --- ELEMENTOS DE LA INTERFAZ ---
    chat_display = ft.Text(value="PROTOCOLO LISTO", color="#00FFFF", size=16)
    
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
        label="COMANDO DE VOZ O TEXTO",
        border_color="#00FFFF",
        color="#00FFFF",
        visible=False,
        on_submit=lambda e: enviar(entrada.value)
    )

    # --- LÓGICA DE ACTIVACIÓN ---
    def activar():
        inicio.visible = False
        interfaz_chat.visible = True
        page.vertical_alignment = "start"
        page.update()
        hablar("Protocolo Midna activado. Leo, estoy a la espera de tus instrucciones.")

    def enviar(txt):
        if not txt: return
        chat_display.value = "PROCESANDO..."
        page.update()
        
        url = "https://general-runtime.voiceflow.com/state/user/" + id_usuario + "/interact"
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
            chat_display.value = "ERROR DE CONEXIÓN AL NÚCLEO"
        
        entrada.value = ""
        page.update()

    # --- ESTRUCTURA DE PANTALLAS ---
    inicio = ft.Column([
        ft.Text("M I D N A", size=50, color="#FF7700", weight="bold"),
        ft.Container(height=20),
        nucleo,
        ft.Text("PRESIONE PARA INICIAR", color="#FF7700")
    ], horizontal_alignment="center")

    interfaz_chat = ft.Column([
        ft.Text("SISTEMA HUD", size=20, color="#00FFFF"),
        caja_chat,
        entrada
    ], visible=False, expand=True)

    page.add(inicio)
    page.add(interfaz_chat)

    # Escucha de nombre "Midna" por JavaScript
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