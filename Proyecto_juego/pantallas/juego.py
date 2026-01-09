import pygame
import random
import globales as gb
import datos
import motor
import interfaz
from . import interfaz_juego 
from . import pantallas_previa as pp

def obtener_notacion(f, c, dimension):
    """Convierte coordenadas (f, c) a formato a1, b2, etc."""
    letras = "abcdefghijklmnopqrstuvwxyz"
    columna = letras[c] if c < len(letras) else str(c)
    # En ajedrez las filas se cuentan de abajo hacia arriba
    fila = dimension - f 
    return f"{columna}{fila}"

def mostrar_pantalla_ods(ventana):
    # ... (Se mantiene igual que la versión anterior)
    mensajes_ods = {
        1: "ODS 1: FIN DE LA POBREZA\nErradicar la pobreza es un acto de justicia. Ayuda a quienes\nmas lo necesitan y apoya el comercio justo.",
        2: "ODS 2: HAMBRE CERO\nNo desperdicies comida. Millones de personas pasan hambre.\nConsume de forma responsable y apoya la agricultura local.",
        3: "ODS 3: SALUD Y BIENESTAR\nUna vida sana es un derecho. Mantente activo, cuida tu mente\ny promueve el acceso a la salud para todos.",
        4: "ODS 4: EDUCACION DE CALIDAD\nLa educación abre puertas. Comparte tus conocimientos\ny apoya a otros en su aprendizaje diario.",
        5: "ODS 5: IGUALDAD DE GENERO\nDerechos iguales para todos. El respeto y la equidad\nson la base de una sociedad justa y prospera."
    }
    ods_id = random.randint(1, 5)
    mensaje_actual = mensajes_ods[ods_id]
    img_ods = None
    for extension in [".jpg", ".png"]:
        try:
            ruta = f"assets/ods/ods_img_{ods_id}{extension}"
            img_ods = pygame.image.load(ruta).convert_alpha()
            img_ods = pygame.transform.scale(img_ods, (350, 350))
            break 
        except: continue
    esperando = True
    while esperando:
        ventana.fill((20, 30, 50))
        fuente_texto = pygame.font.SysFont("Verdana", 22)
        if img_ods:
            rect_img = img_ods.get_rect(center=(gb.ANCHO_VENTANA // 2, gb.ALTO_VENTANA // 2 - 80))
            ventana.blit(img_ods, rect_img)
        lineas = mensaje_actual.split('\n')
        for i, linea in enumerate(lineas):
            txt = fuente_texto.render(linea, True, (255, 255, 255))
            ventana.blit(txt, (gb.ANCHO_VENTANA // 2 - txt.get_width() // 2, gb.ALTO_VENTANA // 2 + 120 + (i * 30)))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); exit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN: esperando = False

def ejecutar(ventana_maestra):
    esta_jugando = True
    while esta_jugando:
        dimension = pp.pantalla_seleccion_dimension(ventana_maestra)
        if dimension is None: return "MENU"
        
        pool = [gb.ID_SESION_JUGADOR_UNO, gb.ID_SESION_JUGADOR_DOS]
        random.shuffle(pool)
        id_b, id_n = pool[0], pool[1]
        nom_b, nom_n = datos.obtener_nombre_jugador(id_b), datos.obtener_nombre_jugador(id_n)
        ficha_b = pp.pantalla_seleccion_pieza(ventana_maestra, nom_b, id_b, True)
        ficha_n = pp.pantalla_seleccion_pieza(ventana_maestra, nom_n, id_n, False)
        
        tablero = motor.crear_matriz_dinamica(dimension)
        puntos = [0, 0] 
        es_turno_blancas, partida_activa = True, True
        fase, posiciones = "COLOCACION", [None, None]
        pieza_sel, movs_posibles = None, []
        historial = ["ESC: Menu", f"{nom_b} vs {nom_n}"]

        while partida_activa:
            ventana_maestra.fill((30, 32, 40))
            interfaz_juego.dibujar_paneles_jugadores(ventana_maestra, [nom_b, ficha_b, puntos[0]], [nom_n, ficha_n, puntos[1]], es_turno_blancas)
            interfaz_juego.dibujar_historial(ventana_maestra, historial)
            interfaz.imprimir_tablero_dinamico(ventana_maestra, tablero, dimension, movs_posibles, es_turno_blancas)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: pygame.quit(); exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: return "MENU"

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    coord = interfaz.convertir_posicion_a_coordenada(evento.pos, dimension)
                    if coord:
                        f, c = int(coord[0]), int(coord[1])
                        
                        if fase == "COLOCACION":
                            if posiciones[0] is None and tablero[f][c] == gb.VACIO:
                                tablero[f][c], posiciones[0] = ficha_b, (f, c)
                                es_turno_blancas = False
                            elif posiciones[1] is None and tablero[f][c] == gb.VACIO:
                                tablero[f][c], posiciones[1] = ficha_n, (f, c)
                                motor.generar_peones_ciegos(tablero, dimension)
                                es_turno_blancas, fase = True, "ACCION"

                        elif fase == "ACCION":
                            if pieza_sel is None:
                                ficha_det = tablero[f][c]
                                if (es_turno_blancas and ficha_det == ficha_b) or (not es_turno_blancas and ficha_det == ficha_n):
                                    pieza_sel = (f, c)
                                    movs_posibles = motor.calcular_movimientos(f, c, ficha_det, dimension, tablero) or []
                            else:
                                if (f, c) in movs_posibles:
                                    # OPERACIÓN: Registro simplificado (Ej: a2 -> a4)
                                    pos_ini = obtener_notacion(pieza_sel[0], pieza_sel[1], dimension)
                                    pos_fin = obtener_notacion(f, c, dimension)
                                    jugador = nom_b if es_turno_blancas else nom_n
                                    historial.append(f"{jugador}: {pos_ini} -> {pos_fin}")

                                    target = tablero[f][c]
                                    ganancia = 10 if (target != gb.VACIO and target not in [ficha_b, ficha_n]) else 0
                                    if es_turno_blancas: puntos[0] += ganancia
                                    else: puntos[1] += ganancia
                                    
                                    tablero[f][c], tablero[pieza_sel[0]][pieza_sel[1]] = tablero[pieza_sel[0]][pieza_sel[1]], gb.VACIO
                                    
                                    if puntos[0] >= 40 or puntos[1] >= 40:
                                        mostrar_pantalla_ods(ventana_maestra) 
                                        ganador = nom_b if puntos[0] >= 40 else nom_n
                                        datos.actualizar_puntos_jugador(id_b if puntos[0] >= 40 else id_n, 0)
                                        if pp.pantalla_fin_partida(ventana_maestra, ganador) != "REINTENTAR": return "MENU"
                                        partida_activa = False
                                    else:
                                        es_turno_blancas = not es_turno_blancas
                                    pieza_sel, movs_posibles = None, []
                                else:
                                    # Mensaje de error simplificado
                                    historial.append("! Jugada invalida")
                                    pieza_sel, movs_posibles = None, []

            pygame.display.flip()
    return "MENU"