import flet as ft

def main(page: ft.Page):
    page.title = "Midna AI"
    page.bgcolor = "#050505"
    page.scroll = "always"

    # 1. El área donde Midna escribe (Respuesta)
    # 'selectable=True' permite que puedas copiar lo que Midna te responda
    respuesta_midna = ft.Text(
        "SISTEMA INICIALIZADO. ESPERANDO COMANDO...", 
        color="#00EAFF", 
        size=16,
        width=400,
        selectable=True 
    )

    # 2. Función que se activa al enviar
    def enviar_mensaje(e):
        if entrada.value:
            user_text = entrada.value
            # Aquí simulamos la respuesta de Midna
            # Luego conectaremos esto a la verdadera inteligencia
            respuesta_midna.value = f"MIDNA RESPONDE A: {user_text}\n\nProcesando información... [Simulación de respuesta larga para probar el ajuste de texto]"
            
            entrada.value = "" # Limpia el cuadro después de enviar
            page.update()

    # 3. Título y Logo
    titulo = ft.Text("INTERFACE MIDNA v1.0", size=25, color="#00EAFF", weight="bold")
    
    gif = ft.Image(
        src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
        width=120,
        height=120
    )

    # 4. Cuadro de entrada (Multilínea)
    entrada = ft.TextField(
        label="Escribe tu duda aquí...",
        multiline=True,
        min_lines=1,
        max_lines=5,
        border_color="#00EAFF",
        color="#00EAFF"
    )

    # 5. Botón de enviar (Forma básica compatible)
    boton = ft.ElevatedButton(
        "ENVIAR A MIDNA", 
        on_click=enviar_mensaje
    )

    # Añadimos todo a la pantalla en orden
    page.add(titulo)
    page.add(gif)
    page.add(ft.Divider(color="#00EAFF")) # Una línea divisoria
    page.add(ft.Text("RESPUESTA DE MIDNA:", color="#00EAFF", weight="bold", size=12))
    page.add(respuesta_midna) # Aquí es donde aparecerá el texto de la IA
    page.add(ft.Divider(color="#00EAFF"))
    page.add(entrada)
    page.add(boton)