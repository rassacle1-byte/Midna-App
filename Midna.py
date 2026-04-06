import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN ---
    page.title = "Midna AI - Comunidad"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111827"
    page.padding = 20
    page.window_width = 450
    page.window_height = 750

    # VARIABLE PARA GUARDAR EL NOMBRE DEL AMIGO
    nombre_usuario = ft.Ref[ft.TextField]()

    # --- ELEMENTOS DE LA INTERFAZ ---
    label_respuesta = ft.Text(
        value="¡Hola! Soy Midna. ¿Cómo te llamas para que podamos empezar?", 
        size=16, 
        color="white",
        text_align=ft.TextAlign.LEFT,
    )

    contenedor_scroll = ft.Column(
        controls=[label_respuesta],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    input_mensaje = ft.TextField(
        label="Tu mensaje...", 
        width=400,
        border_color="#3B82F6",
        border_radius=15,
    )

    input_nombre = ft.TextField(
        ref=nombre_usuario,
        label="Escribe tu nombre aquí primero",
        width=300,
        border_color="#FACC15", # Color amarillo para resaltar
    )

    # --- LÓGICA DE ENVÍO ---
    def enviar_a_midna(e):
        # Si no han puesto nombre, no los deja avanzar
        if not nombre_usuario.current.value:
            label_respuesta.value = "⚠️ ¡Ey! Primero dime tu nombre arriba para saber con quién hablo."
            page.update()
            return

        if not input_mensaje.value:
            return
            
        quien_habla = nombre_usuario.current.value
        mensaje_texto = input_mensaje.value
        
        label_respuesta.value = f"Pensando para {quien_habla}..."
        page.update()

        # Usamos el nombre del usuario para crear una sesión única en Voiceflow
        url_api = f"https://general-runtime.voiceflow.com/state/user/{quien_habla}/interact"
        
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        
        # Le enviamos a Voiceflow el mensaje incluyendo el nombre para que sepa quién es
        payload = {
            "action": {"type": "text", "payload": f"Soy {quien_habla}. {mensaje_texto}"}
        }

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            
            mensaje_final = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            
            # Personalizamos la respuesta con el nombre si la IA no lo hizo
            label_respuesta.value = mensaje_final.strip()
        except:
            label_respuesta.value = "Error al conectar con Midna."
        
        input_mensaje.value = ""
        page.update()

    # --- DISEÑO ---
    page.add(
        ft.Text("🤖 MIDNA AI", size=32, weight="bold", color="#3B82F6"),
        ft.Text("Versión para amigos", size=14, color="gray"),
        ft.Divider(height=10),
        
        # CUADRO DE NOMBRE (Solo lo usan al principio)
        ft.Row([input_nombre], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Container(
            content=contenedor_scroll,
            padding=20,
            bgcolor="#1F2937",
            border_radius=15,
            expand=True,
            border=ft.border.all(1, "#374151")
        ),
        
        ft.Divider(height=10, color="transparent"),
        input_mensaje,
        ft.Container(height=10),
        ft.ElevatedButton(
            "Hablar con Midna", 
            on_click=enviar_a_midna, 
            bgcolor="#3B82F6", 
            color="white",
            width=250
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)