import flet as ft
import requests
import uuid # Esto genera un ID único automático
import os # Para verificar la imagen de fondo

def main(page: ft.Page):
    # --- CONFIGURACIÓN JARVIS 2.0 PROTOCOL ---
    page.title = "MIDNA - PROTOCOLO JARVIS"
    page.theme_mode = ft.ThemeMode.DARK
    # Un negro profundo para el fondo, que resalte el cian
    page.bgcolor = "#000000" 
    page.padding = 30
    # Un poco más ancha para que se vea más imponente en PC
    page.window_width = 500 
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Fuente tipo consola para todo
    page.fonts = {
        "Stark": "https://raw.githubusercontent.com/google/fonts/main/ofl/majormonodisplay/MajorMonoDisplay-Regular.ttf"
    }

    # --- DEFINICIÓN DE COLORES NEÓN ---
    NEON_CYAN = "#00FFFF" # Cian neón Stark Industries
    DARK_BLUE_TRANSPARENT = "#001F3FEE" # Azul oscuro translúcido
    TEXT_GLOW = "0 0 10px #00FFFF" # Efecto de brillo en texto
    GLOW_EFFECT = "0 0 15px #00FFFF" # Efecto de brillo en contenedores

    # --- GENERAR UN ID ÚNICO AUTOMÁTICO PARA MULTIUSUARIO ---
    if not page.session.get("user_id"):
        page.session.set("user_id", str(uuid.uuid4())[:10]) # Crea un ID corto como 'a1b2c3d4'
    user_id = page.session.get("user_id")

    # --- ELEMENTOS DE LA INTERFAZ ---
    # Texto de bienvenida que aparecerá sobre el fondo
    label_respuesta = ft.Text(
        value=f"PROTOCOLO MIDNA INICIADO.\nID SESIÓN: {user_id}\nESPERANDO COMANDOS...", 
        size=16, 
        color=NEON_CYAN,
        font_family="Consolas", # Fuente de terminal
        text_align=ft.TextAlign.LEFT
    )

    # Contenedor con scroll para respuestas largas, con borde neón y fondo translúcido
    contenedor_chat = ft.Container(
        content=ft.Column(
            controls=[label_respuesta],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=20,
        bgcolor="#0A111AEE", # Fondo translúcido profundo
        border=ft.border.all(2, NEON_CYAN), # Borde neón
        border_radius=5, # Esquinas poco redondeadas
        expand=True,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN), # Efecto de brillo exterior
    )

    # Campo de mensaje con estilo tecnológico
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

    # --- LÓGICA DE ENVÍO Y CONEXIÓN CON EL NÚCLEO ---
    def enviar_a_midna(e):
        if not input_mensaje.value:
            return
            
        comando_texto = input_mensaje.value
        label_respuesta.value = f"TRANSMITIENDO AL NÚCLEO CENTRAL..."
        label_respuesta.color = NEON_CYAN # Asegurar color neón
        page.update()

        # Usamos el user_id generado automáticamente para Voiceflow
        url_api = f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact"
        
        headers = {
            "Authorization": "VF.DM.69d04b1f38894b2ad3a462fb.uE519RXQDw24JzZQ", 
            "Content-Type": "application/json"
        }
        
        payload = {
            "action": {"type": "text", "payload": comando_texto}
        }

        try:
            response = requests.post(url_api, json=payload, headers=headers)
            data = response.json()
            
            mensaje_final = ""
            for item in data:
                if item.get("type") in ["text", "speak"]:
                    mensaje_final += item["payload"]["message"] + "\n\n"
            
            if not mensaje_final:
                mensaje_final = "CONEXIÓN ESTABLECIDA. SIN DATOS ADICIONALES."
            
            label_respuesta.value = mensaje_final.strip()
        except Exception as error:
            # Texto rojo para error
            label_respuesta.value = f"❌ ERROR DE ENLACE CON EL NÚCLEO CENTRAL: {str(error)}"
            label_respuesta.color = "#FF4444" 
        
        input_mensaje.value = ""
        page.update()

    # --- LÓGICA DE FONDO (USANDO LA IMAGEN PROPORCIONADA) ---
    # Obtenemos el ID del repositorio para formar la URL de la imagen en GitHub
    repo_owner = "rassacle1-byte" # REEMPLAZA ESTO
    repo_name = "Midna-App"
    # URL de la imagen en GitHub (Asegúrate de haberla subido con el nombre 'fondo_hud.png')
    fondo_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/fondo_hud.png"

    # Verificación de imagen (Opcional, pero recomendable)
    if repo_owner == "tu_usuario_de_github":
        # Ponemos un fondo de color sólido si no se ha configurado el usuario
        layout_principal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("M I D N A", size=48, weight="bold", color=NEON_CYAN, font_family="Stark", shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN)),
                    ft.Text("PROTOCOLO JARVIS SYSTEMS", size=18, color=NEON_CYAN, font_family="Consolas"),
                    ft.Divider(height=10, color="transparent"),
                    
                    # El chat flotante
                    contenedor_chat,
                    
                    ft.Divider(height=20, color="transparent"),
                    input_mensaje,
                    ft.Container(height=15),
                    
                    # Botón con efecto neón Stark
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
            bgcolor="#05070A", # Fondo sólido
            expand=True,
        )
    else:
        # Layout principal CON LA IMAGEN DE FONDO
        layout_principal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("M I D N A", size=48, weight="bold", color=NEON_CYAN, font_family="Stark", shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=NEON_CYAN)),
                    ft.Text("PROTOCOLO JARVIS SYSTEMS", size=18, color=NEON_CYAN, font_family="Consolas"),
                    ft.Divider(height=10, color="transparent"),
                    
                    # El chat flotante translúcido
                    contenedor_chat,
                    
                    ft.Divider(height=20, color="transparent"),
                    input_mensaje,
                    ft.Container(height=15),
                    
                    # Botón con efecto neón Stark
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
            image_src=fondo_url, # Imagen HUD de fondo
            image_fit=ft.ImageFit.COVER, # Que cubra toda la pantalla
            expand=True,
        )

    # --- DISEÑO FINAL DE LA PANTALLA ---
    # Agregamos el layout principal que contiene todo sobre la imagen de fondo
    page.add(layout_principal)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)