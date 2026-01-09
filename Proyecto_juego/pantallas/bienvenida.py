import pygame
import globales as gb

def ejecutar(ventana_principal_juego):
    reloj_controlador_fotogramas = pygame.time.Clock()
    
    # Carga del logo
    imagen_logo_central = gb.cargar_imagen("Logo2.webp", (300, 300))
    
    fuente_titulo_ajedrez = pygame.font.SysFont("Arial Black", 55)
    fuente_instruccion_inicio = pygame.font.SysFont("Consolas", 22)
    
    nivel_transparencia_aparicion = 0
    velocidad_aparicion_suave = 5
    
    numero_fotogramas_transcurridos = 0
    esperando_entrada_usuario = True
    
    while esperando_entrada_usuario:
        # 1. FONDO BASE
        ventana_principal_juego.fill((30, 30, 30)) 
        
        if nivel_transparencia_aparicion < 255:
            nivel_transparencia_aparicion += velocidad_aparicion_suave
            
        posicion_centro_horizontal_logo = gb.ANCHO_VENTANA // 2 - 150
        posicion_vertical_logo = 60
        
        # --- CUADRADO BLANCO DETRÁS DEL LOGO ---
        superficie_cuadrado = pygame.Surface((310, 310), pygame.SRCALPHA)
        pygame.draw.rect(superficie_cuadrado, (255, 255, 255, nivel_transparencia_aparicion), (0, 0, 310, 310))
        ventana_principal_juego.blit(superficie_cuadrado, (posicion_centro_horizontal_logo - 5, posicion_vertical_logo - 5))

        # 2. DIBUJAR LOGO
        if imagen_logo_central:
            imagen_logo_central.set_alpha(nivel_transparencia_aparicion)
            ventana_principal_juego.blit(imagen_logo_central, (posicion_centro_horizontal_logo, posicion_vertical_logo))

        # 3. TÍTULO DEL JUEGO: AJEDREZ UCAB EN AMARILLO
        # Cambiado a (255, 255, 0) para color Amarillo
        superficie_texto_titulo = fuente_titulo_ajedrez.render("AJEDREZ UCAB", True, (255, 255, 0))
        superficie_texto_titulo.set_alpha(nivel_transparencia_aparicion)
        
        posicion_x_titulo = gb.ANCHO_VENTANA // 2 - superficie_texto_titulo.get_width() // 2
        posicion_y_titulo = 380
        ventana_principal_juego.blit(superficie_texto_titulo, (posicion_x_titulo, posicion_y_titulo))
        
        # 4. INSTRUCCIÓN PARPADEANTE
        numero_fotogramas_transcurridos += 1
        frecuencia_parpadeo_texto = (numero_fotogramas_transcurridos // 40) % 2
        
        if frecuencia_parpadeo_texto == 0 and nivel_transparencia_aparicion >= 255:
            superficie_texto_instruccion = fuente_instruccion_inicio.render("PRESIONE CUALQUIER TECLA PARA COMENZAR", True, (220, 220, 220))
            posicion_x_instruccion = gb.ANCHO_VENTANA // 2 - superficie_texto_instruccion.get_width() // 2
            posicion_y_instruccion = 520
            ventana_principal_juego.blit(superficie_texto_instruccion, (posicion_x_instruccion, posicion_y_instruccion))
        
        pygame.display.flip()
        
        for evento_sistema in pygame.event.get():
            if evento_sistema.type == pygame.QUIT:
                return "SALIR"
            if evento_sistema.type == pygame.KEYDOWN or evento_sistema.type == pygame.MOUSEBUTTONDOWN:
                return "MENU"
        
        reloj_controlador_fotogramas.tick(60)