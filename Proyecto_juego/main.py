import pygame
import globales as gb
from pantallas import (
    bienvenida, 
    menu, 
    creditos, 
    registro, 
    login, 
    juego, 
    reportes_visual, 
    pantallas_previa
)

def ejecutar_sistema():
    # 1. INICIALIZACIÓN
    pygame.init()
    pygame.mixer.init()
    
    ventana = pygame.display.set_mode((gb.ANCHO_VENTANA, gb.ALTO_VENTANA))
    pygame.display.set_caption("SISTEMA DE AJEDREZ Y ODS - SEBASTIAN RIVAS")
    
    # 2. CONFIGURACIÓN DE MÚSICA
    try:
        pygame.mixer.music.load("assets/musica.mp3") 
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, fade_ms=2000)
    except pygame.error:
        print("Aviso: No se pudo cargar el archivo de música.")

    # 3. FLUJO PRINCIPAL (SIN BREAKS)
    bienvenida.ejecutar(ventana)
    
    estado = "MENU"
    ejecutando = True
    
    while ejecutando:
        # Control de transiciones por estados
        if estado == "MENU":
            estado = menu.ejecutar(ventana)
        
        elif estado == "REGISTRO":
            estado = registro.ejecutar(ventana)
            
        elif estado == "LOGIN":
            estado = login.ejecutar(ventana)
                
        elif estado == "JUEGO":
            estado = juego.ejecutar(ventana)
            
        elif estado == "REPORTES":
            estado = reportes_visual.ejecutar(ventana)
            
        elif estado == "CREDITOS":
            creditos.ejecutar(ventana)
            estado = "MENU"
            
        elif estado == "SALIR":
            ejecutando = False
            
        # Manejo de cierre inesperado desde la X de la ventana
        for evento in pygame.event.get(pygame.QUIT):
            ejecutando = False

    # 4. FINALIZACIÓN
    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    ejecutar_sistema()
    