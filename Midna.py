import flet as ft
import requests
import uuid # Generador de IDs únicos automáticos

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS 2.0 PROTOCOL ---
    # Usamos las funciones de configuración de página que ya tenías, pero con valores JARVIS
    page.title = "MIDNA - PROTOCOLO JARVIS"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000" # Negro profundo para el fondo
    page.padding = 30
    # Ancho imponente, adaptable a PC y celular
    page.window_width = 500 
    page.window_height = 800
    # Mantenemos las alineaciones que tenías
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Cargamos fuentes futuristas
    page.fonts = {
        "Stark": "https://raw.githubusercontent.com/google/fonts/main/ofl/majormonodisplay/MajorMonoDisplay-Regular.ttf"
    }

    # --- COLORES NEÓN ---
    NEON_CYAN = "#00FFFF" # Cian neón Stark Industries
    DARK_BLUE_TRANSPARENT = "#001F3FEE" # Azul oscuro translúcido
    TEXT_GLOW = "0 0 10px #00FFFF" # Efecto de brillo en texto

    # --- GENERAR UN ID ÚNICO AUTOMÁTICO PARA MULTIUSUARIO ---
    # Mantenemos la lógica de multiusuario automática, sin pedir nombres
    # Esto usa page.session de forma segura para web
    if not page.session.get("user_id"):
        # Crea un ID corto como 'a1b2c3d4'
        page.session.set("user_id", str(uuid.uuid4())[:10]) 
    user_id = page.session.get("user_id")

    # --- ELEMENTOS DE LA INTERFAZ ---
    # Texto de respuesta sobre el fondo. Mantenemos tu label_respuesta pero con estilo JARVIS
    label_respuesta = ft.Text(
        value=f"PROTOCOLO MIDNA INICIADO.\nID SESIÓN: {user_id}\nESPERANDO COMANDOS...", 
        size=16, 
        color=NEON_CYAN,
        font_family="Consolas", # Fuente de terminal
        text_align=ft.TextAlign.LEFT
    )

    # Contenedor con SCROLL para respuestas largas, con borde neón y fondo translúcido
    # Esto soluciona tu problema de que el texto largo se cortaba
    contenedor_chat = ft.Container(
        content=ft.Column(
            controls=[label_respuesta],
            scroll=ft.ScrollMode.AUTO, # Permite deslizar si el texto es largo
            expand=True,
        ),
        padding=20,
        bgcolor="#0A111AEE", # Fondo translúcido profundo para ver el holograma
        border=ft.border.all(2, NEON_CYAN), # Borde neón cian
        border_radius=5, # Esquinas poco redondeadas
        expand=True,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN), # Brillo exterior
    )

    # Mantenemos tu input_mensaje pero con estilo tecnológico
    input_mensaje = ft.TextField(
        label="INTRODUCIR COMANDO...", 
        border_color=NEON_CYAN,
        border_radius=5,
        color=NEON_CYAN,
        label_style=ft.TextStyle(color=NEON_CYAN, font_family="Consolas"),
        cursor_color=NEON_CYAN,
        on_submit=lambda e: enviar_a_midna(e),
        width=450,
        # Translúcido para ver el fondo
        bgcolor="#05070AEE"
    )

    # --- LÓGICA DE ENVÍO Y CONEXIÓN CON TU NÚCLEO DE VOICEFLOW ---
    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        comando_texto = input_mensaje.value
        label_respuesta.value = f"TRANSMITIENDO AL NÚCLEO CENTRAL..."
        label_respuesta.color = NEON_CYAN # Asegurar color neón
        page.update()

        # Usamos el user_id generado automáticamente para Voiceflow
        url_api = f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact"
        
        # Mantenemos las cabeceras exactas de tu código base
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        
        payload = {
            "action": {"type": "text", "payload": comando_texto}
        }

        try:
            # Mantenemos tu requests.post
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            
            # Recorremos la respuesta para juntar todo el texto
            mensaje_final = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            
            if not mensaje_final:
                mensaje_final = "CONEXIÓN ESTABLECIDA. SIN DATOS ADICIONALES."
            
            label_respuesta.value = mensaje_final.strip()
        except Exception as error:
            # Texto rojo para error
            label_respuesta.value = f"❌ ERROR DE ENLACE CON EL NÚCLEO CENTRAL."
            label_respuesta.color = "#FF4444" 
        
        # Mantenemos el limpiar input y update
        input_mensaje.value = ""
        page.update()

    # --- LÓGICA DE FONDO (USANDO TU IMAGEN) ---
    # REEMPLAZA ESTO CON TU USUARIO REAL DE GITHUB
    repo_owner = "rassacle1-byte" 
    repo_name = "Midna-App"
    # URL de la imagen en tu GitHub (fondo_hud.png)
    fondo_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/fondo_hud.png"

    # Layout principal que une todo con el fondo JARVIS
    layout_principal = ft.Container(
        content=ft.Column(
            controls=[
                # Título imponente con fuente Stark y brillo
                ft.Text("M I D N A", size=48, weight="bold", color=NEON_CYAN, font_family="Stark", shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN)),
                ft.Text("PROTOCOLO JARVIS SYSTEMS", size=18, color=NEON_CYAN, font_family="Consolas"),
                ft.Divider(height=10, color="transparent"),
                
                # Mantenemos tu lógica de page.add pero dentro de este layout con fondo
                contenedor_chat,
                
                ft.Divider(height=20, color="transparent"),
                input_mensaje,
                ft.Container(height=15),
                
                # Mantenemos tu Elevated Button pero con estilo neón Stark
                ft.ElevatedButton(
                    "EJECUTAR COMANDO", 
                    on_click=enviar_a_midna, 
                    bgcolor=DARK_BLUE_TRANSPARENT, 
                    color=NEON_CYAN,
                    width=250,
                    height=55,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN), 
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                    )
                ),
                # Pie de página Stark Industries
                ft.Container(height=30),
                ft.Text("© STARK INDUSTRIES - MALIBU POINT - PROTOCOLO AUTOMÁTICO", size=10, color="gray", font_family="Consolas"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=30,
        # Aplicamos el fondo HUD tecnológico
        image_src=fondo_url,
        image_fit=ft.ImageFit.COVER, # Que cubra todo
        expand=True,
    )

    # --- AGREGAR A LA PANTALLA ---
    # Reemplazamos tu page.add por el layout principal
    page.add(layout_principal)

if __name__ == "__main__":
    # Usamos el puerto 8080 para Render
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)