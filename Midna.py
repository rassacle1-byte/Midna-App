import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE LA VENTANA ---
    page.title = "Midna AI - Escritorio"
    page.window_width = 450
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111827"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # --- ELEMENTOS DE LA INTERFAZ ---
    # Etiqueta de texto donde aparecerán las respuestas
    label_respuesta = ft.Text(
        value="¡Hola Leo! Soy Midna. ¿En qué te ayudo hoy con tus estudios?", 
        size=16, 
        color="white",
        text_align=ft.TextAlign.LEFT,
    )

    # ESTO PERMITE BAJAR (SCROLL) CUANDO EL TEXTO ES LARGO
    contenedor_scroll = ft.Column(
        controls=[label_respuesta],
        scroll=ft.ScrollMode.AUTO,
        expand=True, # Ocupa el espacio disponible
    )

    # Cuadro para escribir
    input_mensaje = ft.TextField(
        label="Escribe aquí...", 
        width=400,
        border_color="#3B82F6",
        border_radius=15,
        on_submit=lambda e: enviar_a_midna(e)
    )

    # --- LÓGICA DE CONEXIÓN CON VOICEFLOW ---
    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        texto_usuario = input_mensaje.value
        label_respuesta.value = "Midna está pensando..."
        input_mensaje.value = "" # Limpia el cuadro al enviar
        page.update()

        url_api = "https://general-runtime.voiceflow.com/state/user/leo_nuevo/interact"
        
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        
        payload = {
            "action": {"type": "text", "payload": texto_usuario}
        }

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            
            mensaje_final = ""
            # Recorremos la respuesta para juntar todo el texto que envíe la IA
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            
            if not mensaje_final:
                mensaje_final = "No recibí una respuesta clara de Midna."
            
            label_respuesta.value = mensaje_final.strip()
        except Exception as error:
            label_respuesta.value = f"Error de conexión: {str(error)}"
        
        page.update()

    # --- DISEÑO DE LA PANTALLA ---
    page.add(
        ft.Text("🤖 MIDNA AI", size=32, weight="bold", color="#3B82F6"),
        ft.Divider(height=20, color="transparent"),
        
        # Caja gris que contiene el texto con scroll
        ft.Container(
            content=contenedor_scroll,
            padding=20,
            bgcolor="#1F2937",
            border_radius=15,
            expand=True, # Hace que esta caja crezca para llenar la pantalla
            border=ft.border.all(1, "#374151")
        ),
        
        ft.Divider(height=20, color="transparent"),
        
        # Parte inferior: Input y Botón
        ft.Row(
            controls=[
                input_mensaje,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Container(height=10),
        ft.ElevatedButton(
            "Enviar a Midna", 
            on_click=enviar_a_midna, 
            bgcolor="#3B82F6", 
            color="white",
            width=200,
            height=50
        )
    )

# CONFIGURACIÓN PARA RENDER Y CELULAR
if __name__ == "__main__":
    # Usamos el puerto 8080 que es el estándar de Render
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)