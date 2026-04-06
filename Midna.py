import flet as ft
import requests

def main(page: ft.Page):
    # --- CONFIGURACIÓN ---
    page.title = "Midna AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111827"
    page.padding = 20
    page.window_width = 450
    page.window_height = 750

    # --- ELEMENTOS DE LA INTERFAZ ---
    label_respuesta = ft.Text(
        value="¡Hola! Soy Midna. ¿Cómo te llamas para que podamos empezar?", 
        size=16, 
        color="white"
    )

    contenedor_scroll = ft.Column(
        controls=[label_respuesta],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    input_mensaje = ft.TextField(
        label="Escribe tu mensaje aquí...", 
        border_color="#3B82F6",
        border_radius=15,
        on_submit=lambda e: enviar_a_midna(e)
    )

    # LA BARRA QUE QUEREMOS DESAPARECER
    input_nombre = ft.TextField(
        label="Tu nombre",
        width=250,
        border_color="#FACC15",
        hint_text="Escribe tu nombre para iniciar..."
    )

    # CONTENEDOR DE LA BARRA DE NOMBRE (Para poder ocultarlo todo junto)
    fila_nombre = ft.Row(
        controls=[input_nombre],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=True # Al principio es visible
    )

    # --- LÓGICA DE ENVÍO ---
    def enviar_a_midna(e):
        # 1. Verificar si hay nombre
        if not input_nombre.value:
            label_respuesta.value = "⚠️ Por favor, escribe tu nombre primero para conocernos."
            page.update()
            return

        if not input_mensaje.value:
            return
            
        # 2. OCULTAR LA BARRA DE NOMBRE (Aquí ocurre la magia)
        if fila_nombre.visible:
            fila_nombre.visible = False
            page.update()

        quien_habla = input_nombre.value
        mensaje_texto = input_mensaje.value
        
        label_respuesta.value = f"Midna está respondiendo a {quien_habla}..."
        page.update()

        # 3. CONEXIÓN CON VOICEFLOW
        url_api = f"https://general-runtime.voiceflow.com/state/user/{quien_habla}/interact"
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
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
            
            label_respuesta.value = mensaje_final.strip()
        except:
            label_respuesta.value = "Error de conexión. Inténtalo de nuevo."
        
        input_mensaje.value = ""
        page.update()

    # --- DISEÑO FINAL ---
    page.add(
        ft.Text("🤖 MIDNA AI", size=32, weight="bold", color="#3B82F6"),
        ft.Divider(height=10, color="transparent"),
        
        # Esta es la fila que desaparecerá tras el primer envío
        fila_nombre,
        
        ft.Container(
            content=contenedor_scroll,
            padding=20,
            bgcolor="#1F2937",
            border_radius=15,
            expand=True,
            border=ft.border.all(1, "#374151")
        ),
        
        ft.Divider(height=20, color="transparent"),
        input_mensaje,
        ft.Container(height=10),
        ft.ElevatedButton(
            "Enviar", 
            on_click=enviar_a_midna, 
            bgcolor="#3B82F6", 
            color="white",
            width=150
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)