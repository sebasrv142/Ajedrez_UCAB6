import pygame
import globales as gb
import interfaz

def dibujar_paneles_jugadores(ventana, datos_p1, datos_p2, es_turno_blancas):
    """
    MEJORA: Se encapsuló el dibujo de paneles para reducir la carga en el bucle principal.
    """
    fuente = pygame.font.SysFont("Arial", 14, bold=True)
    ANCHO_PANEL = ((gb.ANCHO_VENTANA - 220) - 30) // 2
    
    # Datos estructurados: [nombre, ficha, puntos, x_pos, es_su_turno]
    jugadores = [
        [datos_p1[0], datos_p1[1], datos_p1[2], 10, es_turno_blancas],
        [datos_p2[0], datos_p2[1], datos_p2[2], 20 + ANCHO_PANEL, not es_turno_blancas]
    ]

    for j in jugadores:
        nombre, ficha, pts, x, activo = j
        color_fondo = (45, 55, 80) if activo else (30, 30, 40)
        color_borde = (0, 255, 0) if activo else (80, 80, 80)
        
        rect = pygame.Rect(x, 10, ANCHO_PANEL, 65)
        pygame.draw.rect(ventana, color_fondo, rect, border_radius=10)
        pygame.draw.rect(ventana, color_borde, rect, 2, border_radius=10)
        
        # Dibujar Texto
        txt_nom = fuente.render(f"J: {nombre}", True, (255, 255, 255))
        ventana.blit(txt_nom, (rect.x + 10, 20))
        
        # MEJORA: Renderizado de pieza escalada al lado del nombre (Traída de interfaz.py)
        img_ficha = interfaz.IMAGENES_PIEZAS.get(ficha)
        if img_ficha:
            img_small = pygame.transform.scale(img_ficha, (30, 30))
            ventana.blit(img_small, (rect.x + txt_nom.get_width() + 15, 12))
            
        ventana.blit(fuente.render(f"FICHA: {ficha} | PTS: {pts}", True, (255, 255, 0)), (rect.x + 10, 42))

def dibujar_historial(ventana, historial):
    """
    MEJORA: Limpieza de lógica de dibujado de bitácora.
    """
    fuente_tit = pygame.font.SysFont("Arial", 14, bold=True)
    fuente_his = pygame.font.SysFont("Consolas", 13)
    x_hist = gb.ANCHO_VENTANA - 220
    
    pygame.draw.rect(ventana, (20, 20, 25), (x_hist, 0, 220, gb.ALTO_VENTANA))
    pygame.draw.line(ventana, (255, 255, 255), (x_hist, 0), (x_hist, gb.ALTO_VENTANA), 1)
    ventana.blit(fuente_tit.render("HISTORIAL", True, (0, 255, 255)), (x_hist + 65, 80))

    y_t = 120
    inicio = max(0, len(historial) - 22)
    for i in range(inicio, len(historial)):
        linea = historial[i]
        col = (150, 255, 150) if "J1" in linea else (150, 150, 255)
        if "---" in linea: col = (255, 255, 0)
        ventana.blit(fuente_his.render(linea, True, col), (x_hist + 15, y_t))
        y_t += 22