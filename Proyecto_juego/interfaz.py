import pygame
import globales as gb

IMAGENES_PIEZAS = {}
IMAGEN_CORONA = None 
ULTIMO_TAMANO_CELDA = 0

def cargar_recursos_graficos(tamano_celda):
    global IMAGEN_CORONA
    """Carga y escala las piezas y la corona para el final."""
    traductor_nombres = {
        'P': 'B_Peon',    'p': 'N_Peon',
        'T': 'B_Torre',   't': 'N_Torre',
        'C': 'B_Caballo', 'c': 'N_Caballo',
        'A': 'B_Alfil',   'a': 'N_Alfil',
        'D': 'B_Dama',    'd': 'N_Dama',
        'R': 'B_Rey',     'r': 'N_Rey'
    }

    for letra, nombre_archivo in traductor_nombres.items():
        try:
            ruta = f"assets/{nombre_archivo}.png"
            imagen = pygame.image.load(ruta).convert_alpha()
            IMAGENES_PIEZAS[letra] = pygame.transform.scale(imagen, (tamano_celda, tamano_celda))
        except:
            IMAGENES_PIEZAS[letra] = None

    try:
        IMAGEN_CORONA = pygame.image.load("assets/corona.png").convert_alpha()
        IMAGEN_CORONA = pygame.transform.scale(IMAGEN_CORONA, (40, 40))
    except:
        IMAGEN_CORONA = None

def dibujar_corona_ganador(ventana, x, y, ancho_texto):
    """Dibuja la corona solo en la pantalla de victoria."""
    if IMAGEN_CORONA:
        pos_x = x + (ancho_texto // 2) - (IMAGEN_CORONA.get_width() // 2)
        pos_y = y - 50 
        ventana.blit(IMAGEN_CORONA, (pos_x, pos_y))

def obtener_letras_guia(n):
    abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    resultado = []
    for i in range(n):
        if i < 26:
            resultado.append(abecedario[i])
        else:
            primera = abecedario[(i // 26) - 1]
            segunda = abecedario[i % 26]
            resultado.append(f"{primera}{segunda}")
    return resultado

def imprimir_tablero_dinamico(ventana, matriz, dimension, sugerencias, es_turno_blancas):
    global ULTIMO_TAMANO_CELDA
    
    # 1. Configuración de dimensiones y márgenes
    ESPACIO_PARA_COORDS = 30 
    MARGEN_IZQUIERDO = 50 + ESPACIO_PARA_COORDS
    MARGEN_SUPERIOR = 100
    ANCHO_BITACORA = 220
    ESPACIO_DISPONIBLE = gb.ANCHO_VENTANA - ANCHO_BITACORA - (MARGEN_IZQUIERDO + 50)
    TAMANO_CELDA = ESPACIO_DISPONIBLE // dimension

    if TAMANO_CELDA != ULTIMO_TAMANO_CELDA:
        IMAGENES_PIEZAS.clear()
        cargar_recursos_graficos(TAMANO_CELDA)
        ULTIMO_TAMANO_CELDA = TAMANO_CELDA

    # --- OPERACIÓN: DIBUJO DEL TABLERO Y COORDENADAS ---
    tam_fuente = 14 if dimension <= 14 else 10
    fuente_coords = pygame.font.SysFont("Verdana", tam_fuente, bold=True)
    lista_letras = obtener_letras_guia(dimension)

    fila = 0
    while fila < dimension:
        # Números laterales
        txt_num = fuente_coords.render(str(dimension - fila), True, (200, 200, 200))
        ventana.blit(txt_num, (MARGEN_IZQUIERDO - 35, MARGEN_SUPERIOR + (fila * TAMANO_CELDA) + (TAMANO_CELDA // 2 - 7)))
        
        columna = 0
        while columna < dimension:
            pos_x = MARGEN_IZQUIERDO + (columna * TAMANO_CELDA)
            pos_y = MARGEN_SUPERIOR + (fila * TAMANO_CELDA)
            rect = pygame.Rect(pos_x, pos_y, TAMANO_CELDA, TAMANO_CELDA)

            # Colores de las celdas
            color_celda = (240, 217, 181) if (fila + columna) % 2 == 0 else (181, 136, 99)
            pygame.draw.rect(ventana, color_celda, rect)
            pygame.draw.rect(ventana, (40, 40, 40), rect, 1)

            # Piezas
            p_matriz = matriz[fila][columna]
            if p_matriz != gb.VACIO and p_matriz in IMAGENES_PIEZAS:
                ventana.blit(IMAGENES_PIEZAS[p_matriz], (pos_x, pos_y))
            
            # Sugerencias de movimiento
            for sug_f, sug_c in sugerencias:
                if sug_f == fila and sug_c == columna:
                    surf = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA), pygame.SRCALPHA)
                    color = (255, 0, 0, 160) if matriz[fila][columna] != gb.VACIO else (0, 255, 0, 160)
                    pygame.draw.circle(surf, color, (TAMANO_CELDA // 2, TAMANO_CELDA // 2), TAMANO_CELDA // 3, 5)
                    ventana.blit(surf, (pos_x, pos_y))
            
            # Letras inferiores
            if fila == dimension - 1:
                txt_l = fuente_coords.render(lista_letras[columna], True, (200, 200, 200))
                ventana.blit(txt_l, (pos_x + (TAMANO_CELDA // 2 - txt_l.get_width() // 2), pos_y + TAMANO_CELDA + 10))
            columna += 1
        fila += 1

def convertir_posicion_a_coordenada(pos_mouse, dimension):
    ESPACIO_PARA_COORDS = 30
    MARGEN_IZQUIERDO = 50 + ESPACIO_PARA_COORDS
    MARGEN_SUPERIOR = 100
    ANCHO_BITACORA = 220
    ESPACIO_DISPONIBLE = gb.ANCHO_VENTANA - ANCHO_BITACORA - (MARGEN_IZQUIERDO + 50)
    TAMANO_CELDA = ESPACIO_DISPONIBLE // dimension
    x, y = pos_mouse
    if MARGEN_IZQUIERDO <= x <= MARGEN_IZQUIERDO + (dimension * TAMANO_CELDA) and \
       MARGEN_SUPERIOR <= y <= MARGEN_SUPERIOR + (dimension * TAMANO_CELDA):
        return int((y - MARGEN_SUPERIOR) // TAMANO_CELDA), int((x - MARGEN_IZQUIERDO) // TAMANO_CELDA)
    return None

def convertir_a_texto(fila, columna, dimension):
    letras = obtener_letras_guia(dimension)
    return f"{letras[columna]}{dimension - fila}"