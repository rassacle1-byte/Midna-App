import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE LA VENTANA ---
    page.title = "Midna AI - Escritorio"
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111827"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- ELEMENTOS DE LA INTERFAZ ---
    label_respuesta = ft.Text(
        value="¡Hola Leo! Soy Midna. ¿En qué te ayudo hoy?", 
        size=16, 
        color="white",
        text_align=ft.TextAlign.CENTER
    )
    
    input_mensaje = ft.TextField(
        label="Escribe aquí...", 
        width=350,
        border_color="#3B82F6",
        on_submit=lambda e: enviar_a_midna(e)
    )

    # --- LÓGICA DE CONEXIÓN ---
    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        label_respuesta.value = "Midna está pensando..."
        page.update()

        url_api = "https://general-runtime.voiceflow.com/state/user/leo_nuevo/interact"
        
        # AQUÍ YA PUSE TU API KEY
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        
        payload = {
            "action": {"type": "text", "payload": input_mensaje.value}
        }

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            
            # Buscamos el mensaje de texto en la respuesta de Voiceflow
            mensaje_final = "No recibí respuesta de la IA."
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final = item["payload"]["message"]
                    break
            
            label_respuesta.value = mensaje_final
        except:
            label_respuesta.value = "Error: No se pudo conectar con Midna."
        
        input_mensaje.value = ""
        page.update()

    # --- AGREGAR A LA PANTALLA ---
    page.add(
        ft.Text("🤖 MIDNA AI", size=30, weight="bold", color="#3B82F6"),
        ft.Container(height=20),
        ft.Container(
            content=label_respuesta,
            padding=20,
            bgcolor="#1F2937",
            border_radius=10
        ),
        ft.Container(height=20),
        input_mensaje,
        ft.ElevatedButton("Enviar a Midna", on_click=enviar_a_midna, bgcolor="#3B82F6", color="white")
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)