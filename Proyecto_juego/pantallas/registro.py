import pygame
import globales as gb
import struct
from . import logica_registro as logica

def dibujar_campo_entrada(ventana, posicion_x, posicion_y, ancho_recuadro, etiqueta_texto, valor_actual, esta_activo, mensaje_error, mostrar_texto_real, posicion_cursor):
    fuente_etiqueta = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_error = pygame.font.SysFont("Arial", 14, italic=True)
    color_borde = (0, 120, 215) if esta_activo else (200, 0, 0) if mensaje_error else (50, 50, 50)
    
    superficie_etiqueta = fuente_etiqueta.render(etiqueta_texto, True, (30, 30, 30))
    ventana.blit(superficie_etiqueta, (posicion_x, posicion_y - 25))
    
    pygame.draw.rect(ventana, (255, 255, 255), (posicion_x, posicion_y, ancho_recuadro, 35))
    pygame.draw.rect(ventana, color_borde, (posicion_x, posicion_y, ancho_recuadro, 35), 2 if esta_activo else 1)
    
    texto_visible = valor_actual if mostrar_texto_real else "*" * len(valor_actual)
    superficie_texto = fuente_etiqueta.render(texto_visible, True, (0, 0, 0))
    ventana.blit(superficie_texto, (posicion_x + 8, posicion_y + 8))

    if esta_activo and (pygame.time.get_ticks() // 500) % 2 == 0:
        ancho_texto_antes = fuente_etiqueta.size(texto_visible[:posicion_cursor])[0]
        pygame.draw.line(ventana, (0, 0, 0), (posicion_x + 8 + ancho_texto_antes, posicion_y + 6), (posicion_x + 8 + ancho_texto_antes, posicion_y + 28), 2)

    if mensaje_error and esta_activo:
        superficie_error = fuente_error.render(mensaje_error, True, (200, 0, 0))
        ventana.blit(superficie_error, (posicion_x + ancho_recuadro + 15, posicion_y + 8))

def mostrar_menu_confirmacion(ventana, pregunta_texto):
    fuente_pregunta = pygame.font.SysFont("Arial", 20, bold=True)
    recuadro_confirmacion = pygame.Rect(200, 250, 400, 150)
    respuesta = None
    while respuesta is None:
        pygame.draw.rect(ventana, (255, 255, 255), recuadro_confirmacion, border_radius=10)
        pygame.draw.rect(ventana, (0, 0, 0), recuadro_confirmacion, 3, border_radius=10)
        texto_render = fuente_pregunta.render(pregunta_texto, True, (0, 0, 0))
        texto_opciones = fuente_pregunta.render("[S] Sí    [N] No", True, (0, 100, 0))
        ventana.blit(texto_render, (recuadro_confirmacion.centerx - texto_render.get_width()//2, recuadro_confirmacion.y + 40))
        ventana.blit(texto_opciones, (recuadro_confirmacion.centerx - texto_opciones.get_width()//2, recuadro_confirmacion.y + 85))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s: respuesta = True
                elif evento.key == pygame.K_n: respuesta = False
    return respuesta

def ejecutar(ventana):
    reloj_fotogramas = pygame.time.Clock()
    fuente_instrucciones = pygame.font.SysFont("Consolas", 14, bold=True)
    proximo_estado = "REGISTRO"
    
    while proximo_estado == "REGISTRO":
        lista_campos = [["Cédula:", "", 180, False], ["Nombre:", "", 280, False], ["Sexo (M/F):", "", 60, False], ["Fecha:", "", 150, False], ["Correo:", "", 280, False], ["Clave (Ver 'V'):", "", 180, True]]
        indice_activo, pos_cursor, msj_error, formulario_terminado = 0, 0, "", False

        while not formulario_terminado:
            ventana.fill((235, 235, 235))
            pygame.draw.rect(ventana, (255, 255, 255), (40, 20, 720, 560), border_radius=15)
            pygame.draw.rect(ventana, (0, 0, 0), (40, 20, 720, 560), 2, border_radius=15)
            guia = fuente_instrucciones.render("[FLECHAS] Navegar | [ENTER] Guardar Final | [ESC] Salir", True, (255, 255, 255))
            pygame.draw.rect(ventana, (40, 40, 40), (40, 540, 720, 40), border_bottom_left_radius=12, border_bottom_right_radius=12)
            ventana.blit(guia, (gb.ANCHO_VENTANA//2 - guia.get_width()//2, 550))
            
            ver_clave = pygame.key.get_pressed()[pygame.K_v]
            y_pos = 80
            for i in range(len(lista_campos)):
                dibujar_campo_entrada(ventana, 80, y_pos, lista_campos[i][2], lista_campos[i][0], lista_campos[i][1], indice_activo == i, msj_error if i == indice_activo else "", (i != 5 or ver_clave), pos_cursor)
                y_pos += 75
            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    formulario_terminado, proximo_estado = True, "SALIR"
                
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        formulario_terminado, proximo_estado = True, "MENU"
                    
                    # --- NAVEGACIÓN LIBRE CON FLECHAS ---
                    elif ev.key == pygame.K_UP:
                        indice_activo = (indice_activo - 1) % len(lista_campos)
                        pos_cursor = len(lista_campos[indice_activo][1])
                        msj_error = ""
                    elif ev.key == pygame.K_DOWN:
                        indice_activo = (indice_activo + 1) % len(lista_campos)
                        pos_cursor = len(lista_campos[indice_activo][1])
                        msj_error = ""
                    elif ev.key == pygame.K_RIGHT and pos_cursor < len(lista_campos[indice_activo][1]):
                        pos_cursor += 1
                    elif ev.key == pygame.K_LEFT and pos_cursor > 0:
                        pos_cursor -= 1
                    
                    # --- VALIDACIÓN Y GUARDADO ---
                    elif ev.key in [pygame.K_TAB, pygame.K_RETURN]:
                        valido, error = logica.validar_campo_actual(indice_activo, lista_campos[indice_activo][1])
                        if valido:
                            msj_error = ""
                            if indice_activo < 5: 
                                indice_activo += 1
                                pos_cursor = len(lista_campos[indice_activo][1])
                            else:
                                # Proceso directo de guardado (Eliminada pregunta "¿Otro?")
                                ced, nom, sex, fec, cor, cla = [c[1].strip() for c in lista_campos]
                                if mostrar_menu_confirmacion(ventana, "¿Encriptar clave?"):
                                    cla = logica.transformar_clave_a_encriptada(cla)
                                
                                reg = struct.pack(gb.FORMATO_ESTRUCTURA_USUARIO, ced.encode('utf-8'), nom.encode('utf-8'), sex.encode('utf-8'), fec.encode('utf-8'), cor.encode('utf-8'), cla.encode('utf-8'))
                                with open(gb.ARCHIVO_USUARIOS, "ab") as f: f.write(reg)
                                
                                proximo_estado = "MENU"
                                formulario_terminado = True
                        else:
                            msj_error = error
                    
                    elif ev.key == pygame.K_BACKSPACE and pos_cursor > 0:
                        lista_campos[indice_activo][1] = lista_campos[indice_activo][1][:pos_cursor-1] + lista_campos[indice_activo][1][pos_cursor:]
                        pos_cursor -= 1
                    
                    elif ev.unicode.isprintable() and len(lista_campos[indice_activo][1]) < 30:
                        if not (ev.key == pygame.K_v and indice_activo == 5):
                            if indice_activo == 0 and not (ev.unicode.isdigit() or ev.unicode == "."):
                                msj_error = "Solo números y puntos"
                            else:
                                lista_campos[indice_activo][1] = lista_campos[indice_activo][1][:pos_cursor] + ev.unicode + lista_campos[indice_activo][1][pos_cursor:]
                                pos_cursor += 1
                                msj_error = ""
            reloj_fotogramas.tick(30)
            
    return proximo_estado