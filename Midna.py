import flet as ft
import requests
import uuid # Genera IDs únicos para que sea multiusuario

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE LA VENTANA ---
    page.title = "Midna AI"
    page.window_width = 400
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111827"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # CREAR ID DE SESIÓN AUTOMÁTICO (Sin nombres manuales)
    if not page.session.get("user_id"):
        page.session.set("user_id", str(uuid.uuid4())[:8])
    user_id = page.session.get("user_id")

    # --- ELEMENTOS DE LA INTERFAZ ---
    label_respuesta = ft.Text(
        value="¡Hola! Soy Midna. ¿En qué puedo ayudarte?", 
        size=16, 
        color="white",
        text_align=ft.TextAlign.LEFT
    )
    
    # Contenedor con SCROLL para textos muy grandes
    contenedor_scroll = ft.Container(
        content=ft.Column(
            controls=[label_respuesta],
            scroll=ft.ScrollMode.AUTO, # Permite bajar si el texto es largo
            expand=True,
        ),
        padding=20,
        bgcolor="#1F2937",
        border_radius=10,
        expand=True, 
        width=350,
        height=450 
    )
    
    input_mensaje = ft.TextField(
        label="Escribe un comando...", 
        width=350,
        border_color="#3B82F6",
        focused_border_color="#3B82F6",
        on_submit=lambda e: enviar_a_midna(e)
    )

    # --- LÓGICA DE CONEXIÓN ---
    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        label_respuesta.value = "Procesando..."
        page.update()

        # Usamos el ID generado automáticamente para la conexión
        url_api = f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact"
        
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
            
            # Unimos todos los fragmentos de texto si la respuesta es muy larga
            mensaje_completo = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_completo += item["payload"]["message"] + "\n\n"
            
            label_respuesta.value = mensaje_completo.strip() if mensaje_completo else "Sistema listo."
        except:
            label_respuesta.value = "Error: Fallo de conexión con el núcleo."
        
        input_mensaje.value = ""
        page.update()

    # --- AGREGAR A LA PANTALLA ---
    page.add(
        ft.Text("🤖 MIDNA AI", size=30, weight="bold", color="#3B82F6"),
        ft.Container(height=10),
        contenedor_scroll, 
        ft.Container(height=10),
        input_mensaje,
        ft.ElevatedButton(
            "Enviar", 
            on_click=enviar_a_midna, 
            bgcolor="#3B82F6", 
            color="white",
            width=200
        )
    )

if __name__ == "__main__":
    # Render necesita el puerto 8080 para funcionar en la web
    ft.app(target=main, port=8080, view=ft.AppView.WEB_BROWSER)