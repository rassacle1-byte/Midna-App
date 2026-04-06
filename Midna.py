import flet as ft
import requests
import uuid

def main(page: ft.Page):
    # --- CONFIGURACIÓN ESTILO JARVIS ---
    page.title = "MIDNA - INTERFAZ JARVIS"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#05070A" # Negro azulado muy oscuro
    page.padding = 20
    page.window_width = 450
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Colores Neón Stark
    NEON_CYAN = "#00FFFF"
    DARK_BLUE = "#001F3F"

    # Generar ID único automático por sesión (Multiusuario sin nombres)
    if not page.session.get("user_id"):
        page.session.set("user_id", str(uuid.uuid4())[:8].upper())
    
    user_id = page.session.get("user_id")

    # --- ELEMENTOS DE LA INTERFAZ ---
    
    # Etiqueta de respuesta (dentro del contenedor con scroll)
    label_respuesta = ft.Text(
        value=f"SISTEMA ONLINE.\nID_SESIÓN: {user_id}\nESPERANDO COMANDOS...", 
        size=16, 
        color=NEON_CYAN,
        font_family="Consolas" # Fuente tipo terminal
    )

    # Contenedor de Chat con SCROLL (Para textos largos)
    contenedor_chat = ft.Container(
        content=ft.Column(
            controls=[label_respuesta],
            scroll=ft.ScrollMode.AUTO, # Aquí activamos el scroll
            expand=True,
        ),
        padding=20,
        bgcolor="#0A111A", # Fondo del cuadro de texto
        border=ft.border.all(2, NEON_CYAN), # Borde de neón
        border_radius=10,
        expand=True,
        # Sombra para dar efecto de brillo (glow)
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=NEON_CYAN),
    )

    # Campo de entrada de texto
    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", 
        border_color=NEON_CYAN,
        color=NEON_CYAN,
        label_style=ft.TextStyle(color=NEON_CYAN, font_family="Consolas"),
        on_submit=lambda e: enviar_a_midna(e),
        width=400,
    )

    # --- LÓGICA DE ENVÍO ---
    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        comando_texto = input_mensaje.value
        label_respuesta.value = "PROCESANDO..."
        page.update()

        url_api = f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact"
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        payload = {"action": {"type": "text", "payload": comando_texto}}

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            
            mensaje_final = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            
            label_respuesta.value = mensaje_final.strip()
        except:
            label_respuesta.value = "❌ ERROR: FALLO EN EL NÚCLEO CENTRAL."
        
        input_mensaje.value = ""
        page.update()

    # --- AGREGAR A LA PANTALLA ---
    page.add(
        ft.Text("M I D N A", size=40, weight="bold", color=NEON_CYAN, font_family="Consolas"),
        ft.Text("SYSTEMS PROTOCOL", size=14, color=NEON_CYAN),
        ft.Divider(height=20, color="transparent"),
        
        contenedor_chat, # La caja con scroll
        
        ft.Divider(height=20, color="transparent"),
        input_mensaje,
        ft.Container(height=10),
        
        ft.ElevatedButton(
            "EJECUTAR COMANDO", 
            on_click=enviar_a_midna, 
            bgcolor=DARK_BLUE, 
            color=NEON_CYAN,
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        ),
        ft.Container(height=20),
        ft.Text("© STARK INDUSTRIES", size=10, color="gray")
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)