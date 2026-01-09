import pygame
import globales as gb
import interfaz  # Importamos para usar la corona

def pantalla_seleccion_dimension(ventana):
    fuente_titulo = pygame.font.SysFont("Arial", 30, bold=True)
    fuente_input = pygame.font.SysFont("Arial", 40, bold=True)
    fuente_ayuda = pygame.font.SysFont("Arial", 18)
    
    texto_usuario = ""
    error_msj = ""
    input_rect = pygame.Rect(gb.ANCHO_VENTANA // 2 - 50, 250, 100, 60)
    
    while True:
        ventana.fill((30, 32, 40))
        
        txt_titulo = fuente_titulo.render("INGRESA EL TAMAÑO DEL TABLERO", True, (255, 255, 255))
        txt_rango = fuente_ayuda.render("Rango permitido: 5 a 32", True, (200, 200, 200))
        txt_instruccion = fuente_ayuda.render("Escribe el número y presiona ENTER", True, (150, 150, 150))
        
        ventana.blit(txt_titulo, (gb.ANCHO_VENTANA // 2 - txt_titulo.get_width() // 2, 120))
        ventana.blit(txt_rango, (gb.ANCHO_VENTANA // 2 - txt_rango.get_width() // 2, 170))
        ventana.blit(txt_instruccion, (gb.ANCHO_VENTANA // 2 - txt_instruccion.get_width() // 2, gb.ALTO_VENTANA - 80))

        pygame.draw.rect(ventana, (50, 50, 60), input_rect, border_radius=10)
        pygame.draw.rect(ventana, (0, 255, 0), input_rect, 2, border_radius=10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if texto_usuario.isdigit():
                        valor = int(texto_usuario)
                        if 5 <= valor <= 32: return valor
                        else: error_msj = "Fuera de rango (5-32)"
                    else: error_msj = "Ingresa un número"
                    texto_usuario = "" 
                
                elif evento.key == pygame.K_BACKSPACE:
                    texto_usuario = texto_usuario[:-1]
                
                elif evento.unicode.isdigit() and len(texto_usuario) < 2:
                    texto_usuario += evento.unicode
                    error_msj = ""

        txt_surface = fuente_input.render(texto_usuario, True, (255, 255, 255))
        ventana.blit(txt_surface, (input_rect.x + (input_rect.width // 2 - txt_surface.get_width() // 2), input_rect.y + 5))
        
        if error_msj:
            txt_error = fuente_ayuda.render(error_msj, True, (255, 80, 80))
            ventana.blit(txt_error, (gb.ANCHO_VENTANA // 2 - txt_error.get_width() // 2, 330))

        pygame.display.flip()

def pantalla_seleccion_pieza(ventana, nombre_jugador, id_jugador, es_blancas):
    fuente_titulo = pygame.font.SysFont("Arial", 25, bold=True)
    fuente_piezas = pygame.font.SysFont("Arial", 18, bold=True)
    
    if es_blancas:
        opciones = [('Torre', 'T', 'B_Torre'), ('Caballo', 'C', 'B_Caballo'), 
                    ('Alfil', 'A', 'B_Alfil'), ('Dama', 'D', 'B_Dama'), ('Rey', 'R', 'B_Rey')]
    else:
        opciones = [('Torre', 't', 'N_Torre'), ('Caballo', 'c', 'N_Caballo'), 
                    ('Alfil', 'a', 'N_Alfil'), ('Dama', 'd', 'N_Dama'), ('Rey', 'r', 'N_Rey')]
        
    imagenes_seleccion = []
    for nombre, letra, archivo in opciones:
        try:
            img = pygame.image.load(f"assets/{archivo}.png").convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            imagenes_seleccion.append(img)
        except: imagenes_seleccion.append(None)
            
    indice = 0
    while True:
        ventana.fill((30, 32, 40))
        titulo = fuente_titulo.render(f"{nombre_jugador}, elige tu pieza", True, (255, 255, 255))
        ventana.blit(titulo, (gb.ANCHO_VENTANA // 2 - titulo.get_width() // 2, 80))
        
        ancho_total_opciones = len(opciones) * 130 
        x_inicio = (gb.ANCHO_VENTANA - ancho_total_opciones) // 2 + 30

        for i, (nombre, letra, archivo) in enumerate(opciones):
            x_pos = x_inicio + (i * 130) 
            y_pos = 220
            rect = pygame.Rect(x_pos - 20, y_pos - 15, 100, 130)
            
            color_recuadro = (0, 255, 0) if i == indice else (70, 70, 80)
            pygame.draw.rect(ventana, color_recuadro, rect, 3, border_radius=10)
            
            if imagenes_seleccion[i]:
                ventana.blit(imagenes_seleccion[i], (rect.centerx - 30, y_pos))
            else:
                txt_letra = fuente_piezas.render(letra, True, (255, 255, 255))
                ventana.blit(txt_letra, (rect.centerx - txt_letra.get_width() // 2, y_pos + 20))
                
            txt_nom = fuente_piezas.render(nombre, True, (255, 255, 255) if i == indice else (200, 200, 200))
            ventana.blit(txt_nom, (rect.centerx - txt_nom.get_width() // 2, y_pos + 85))
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT: indice = (indice - 1) % len(opciones)
                if evento.key == pygame.K_RIGHT: indice = (indice + 1) % len(opciones)
                if evento.key == pygame.K_RETURN: return opciones[indice][1]
        pygame.display.flip()

def pantalla_fin_partida(ventana, ganador):
    fuente_fin = pygame.font.SysFont("Arial", 40, bold=True)
    fuente_opcion = pygame.font.SysFont("Arial", 25)
    opciones = ["REINTENTAR", "MENU PRINCIPAL"]
    indice = 0
    
    while True:
        ventana.fill((20, 20, 30))
        
        # Renderizado del texto del ganador
        txt_ganador = fuente_fin.render(f"¡GANADOR: {ganador}!", True, (255, 255, 0))
        x_ganador = gb.ANCHO_VENTANA // 2 - txt_ganador.get_width() // 2
        y_ganador = 180 # Bajamos un poco el texto para que quepa la corona arriba
        
        # --- OPERACIÓN: DIBUJAR CORONA ---
        # Llamamos a la función de interfaz.py que configuramos antes
        interfaz.dibujar_corona_ganador(ventana, x_ganador, y_ganador, txt_ganador.get_width())
        
        ventana.blit(txt_ganador, (x_ganador, y_ganador))
        
        for i, opt in enumerate(opciones):
            color = (0, 255, 0) if i == indice else (255, 255, 255)
            txt_opt = fuente_opcion.render(opt, True, color)
            ventana.blit(txt_opt, (gb.ANCHO_VENTANA // 2 - txt_opt.get_width() // 2, 330 + (i * 60)))
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP: indice = (indice - 1) % len(opciones)
                if evento.key == pygame.K_DOWN: indice = (indice + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    return "REINTENTAR" if indice == 0 else "MENU"
        pygame.display.flip()