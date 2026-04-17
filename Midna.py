import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN PARA VERSIONES ANTIGUAS ---
    page.title = "MIDNA"
    page.bgcolor = "#00050A"
    
    # ID simple para que Voiceflow te reconozca
    id_usr = str(uuid.uuid4())[:8]

    # --- FUNCIÓN: VOZ ---
    def hablar(texto):
        t = texto.replace("'", "").replace("\n", " ")
        page.run_javascript("window.speechSynthesis.speak(new SpeechSynthesisUtterance('" + t + "'));")

    # --- DISEÑO DEL NÚCLEO (Solo un botón naranja gigante) ---
    # Eliminamos 'alignment' que causó el error en 1000237041.jpg
    nucleo = ft.Container(
        content=ft.Text("ACTIVAR", color="white", weight="bold"),
        width=150,
        height=150,
        bgcolor="#FF7700",
        border_radius=75,
        on_click=lambda _: activar()
    )

    # --- INTERFAZ DE CHAT ---
    respuesta_txt = ft.Text(value="SISTEMA LISTO", color="#00FFFF")
    
    caja_chat = ft.Container(
        content=ft.Column([respuesta_txt], scroll="auto"),
        padding=10,
        bgcolor="#050F1A",
        border_radius=5,
        visible=False
    )

    entrada = ft.TextField(
        label="Comando...",
        visible=False,
        on_submit=lambda e: enviar(entrada.value)
    )

    # --- LÓGICA ---
    def activar():
        inicio.visible = False
        chat.visible = True
        page.update()
        hablar("Midna en línea.")

    def enviar(txt):
        if not txt: return
        respuesta_txt.value = "..."
        page.update()
        
        url = "https://general-runtime.voiceflow.com/state/user/" + id_usr + "/interact"
        headers = {"Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ"}
        payload = {"action": {"type": "text", "payload": txt}}

        try:
            r = requests.post(url, json=payload, headers=headers).json()
            msg = ""
            for item in r:
                if "payload" in item and "message" in item["payload"]:
                    msg += item["payload"]["message"] + " "
            respuesta_txt.value = msg.strip()
            hablar(respuesta_txt.value)
        except:
            respuesta_txt.value = "Error de red."
        
        entrada.value = ""
        page.update()

    # --- VISTAS ---
    inicio = ft.Column([
        ft.Text("M I D N A", size=40, color="#FF7700"),
        nucleo
    ])

    chat = ft.Column([
        ft.Text("HUD AZUL", color="#00FFFF"),
        caja_chat,
        entrada
    ], visible=False)

    page.add(inicio)
    page.add(chat)

if __name__ == "__main__":
    ft.app(target=main)