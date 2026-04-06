import flet as ft

def main(page: ft.Page):
    page.bgcolor = "#050505"
    page.scroll = "always"

    # Componentes simplificados al máximo
    # En versiones muy viejas, el texto del botón se pasa como primer argumento sin 'text='
    
    def al_hacer_clic(e):
        print("Enviado")
        entrada.value = ""
        page.update()

    # Usamos controles sin nombres de argumentos complicados
    titulo = ft.Text("SISTEMA MIDNA", size=30, color="#00EAFF")
    
    # Campo de texto multilínea
    entrada = ft.TextField(
        multiline=True,
        min_lines=1,
        max_lines=10,
        border_color="#00EAFF",
        color="#00EAFF"
    )

    # Botón en su forma más básica
    boton = ft.ElevatedButton(
        "ENVIAR", 
        on_click=al_hacer_clic
    )

    # Imagen simple
    gif = ft.Image(
        src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm5ueHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JnB0PWExJmU9ZSZmPTE/3o7TKMGpxx6676GZ8Y/giphy.gif",
        width=150,
        height=150
    )

    # Añadir todo a la página uno por uno para evitar fallos de contenedores
    page.add(titulo)
    page.add(gif)
    page.add(ft.Text("ESCRIBE TU COMANDO:", color="#00EAFF"))
    page.add(entrada)
    page.add(boton)

    page.update()

ft.app(target=main)