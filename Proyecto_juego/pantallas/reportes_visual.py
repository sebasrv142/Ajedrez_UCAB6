import pygame
import sys
import globales as gb
from . import procesamiento_datos as proc

def dibujar_cabecera(ventana, titulo, f_tit):
    pygame.draw.rect(ventana, (20, 20, 25), (0, 0, 800, 80))
    pygame.draw.line(ventana, (212, 175, 55), (0, 80), (800, 80), 2)
    ventana.blit(f_tit.render(titulo, True, (212, 175, 55)), (30, 20))

def dibujar_barra_guia(ventana, texto, f_txt):
    pygame.draw.rect(ventana, (25, 25, 30), (0, 560, 800, 40))
    pygame.draw.line(ventana, (100, 100, 100), (0, 560), (800, 560), 1)
    ventana.blit(f_txt.render(texto, True, (180, 180, 180)), (20, 570))

def ejecutar(ventana):
    f_tit = pygame.font.SysFont("Segoe UI", 32, bold=True)
    f_btn = pygame.font.SysFont("Segoe UI", 22)
    f_txt = pygame.font.SysFont("Consolas", 16)
    reloj = pygame.time.Clock()
    
    estado = "MENU"
    opciones = ["Ranking de Jugadores", "Historial por Usuario", "Volver"]
    sel, scroll_y = 0, 0
    input_ced = ""
    lista_a, res_b = [], (None, [])
    
    ejecutando = True
    while ejecutando:
        ventana.fill((30, 32, 40))
        guia_actual = ""
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    if estado == "MENU": ejecutando = False
                    else: estado = "MENU"; scroll_y = 0
                if estado == "MENU":
                    if ev.key == pygame.K_UP: sel = (sel - 1) % len(opciones)
                    if ev.key == pygame.K_DOWN: sel = (sel + 1) % len(opciones)
                    if ev.key == pygame.K_RETURN:
                        scroll_y = 0
                        if sel == 0: 
                            estado = "A"
                            lista_a = proc.obtener_datos_reporte_a()
                        elif sel == 1: 
                            estado = "B"
                            input_ced = ""; res_b = (None, [])
                        elif sel == 2: ejecutando = False
                elif estado == "B":
                    if ev.key == pygame.K_RETURN: res_b = proc.buscar_jugador_b(input_ced)
                    elif ev.key == pygame.K_BACKSPACE: input_ced = input_ced[:-1]
                    elif ev.unicode.isdigit() or ev.unicode == ".": input_ced += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 4: scroll_y = min(0, scroll_y + 40)
                if ev.button == 5: scroll_y -= 40

        if estado == "MENU":
            guia_actual = "[FLECHAS]: Navegar | [ENTER]: Seleccionar | [ESC]: Salir"
            ventana.blit(f_tit.render("ESTADÍSTICAS DEL SISTEMA", True, (212, 175, 55)), (50, 50))
            for i, opt in enumerate(opciones):
                rect_y = 160 + i*70
                color_bg = (212, 175, 55) if i == sel else (45, 48, 60)
                pygame.draw.rect(ventana, color_bg, (50, rect_y, 400, 50), border_radius=8)
                ventana.blit(f_btn.render(opt, True, (20,20,20) if i==sel else (200,200,200)), (80, rect_y + 10))
        elif estado == "A":
            guia_actual = "[MOUSE]: Scroll | [ESC]: Volver al menú"
            dibujar_cabecera(ventana, "RANKING DE PUNTUACIONES", f_tit)
            tit = f"{'POS':4} | {'NOMBRE':18} | {'CEDULA':14} | {'PTS':6} | {'JUEGOS'}"
            ventana.blit(f_txt.render(tit, True, (212, 175, 55)), (50, 95))
            for i, j in enumerate(lista_a):
                y = 135 + i*40 + scroll_y
                if 110 < y < 550:
                    pygame.draw.rect(ventana, (40, 42, 55), (30, y, 740, 32), border_radius=5)
                    txt = f"#{i+1:02} | {j['nom'][:18]:18} | {j['ced']:14} | {j['puntos']:6} | {j['part']:02} Jgs"
                    ventana.blit(f_txt.render(txt, True, (240, 240, 240)), (50, y + 6))
        elif estado == "B":
            guia_actual = "[TECLADO]: C.I | [ENTER]: Buscar | [ESC]: Volver"
            dibujar_cabecera(ventana, "CONSULTA POR CÉDULA", f_tit)
            ventana.blit(f_txt.render(f"Introduzca C.I: {input_ced}|", True, (255, 255, 255)), (50, 110))
            if res_b[0]:
                y_box = 160
                pygame.draw.rect(ventana, (45, 48, 60), (50, y_box, 700, 110), border_radius=10)
                detalles = [f"Nombre: {res_b[0]['nom']}", f"Cédula: {res_b[0]['ced']}", f"Puntaje: {res_b[0]['pts']} pts", f"Sexo: {res_b[0]['sex']} | Fecha: {res_b[0]['fec']}"]
                for k, t in enumerate(detalles):
                    ventana.blit(f_txt.render(t, True, (212, 175, 55)), (70, y_box + 12 + k*22))
                ventana.blit(f_txt.render("HISTORIAL:", True, (255, 255, 255)), (50, 290))
                for i, p in enumerate(res_b[1]):
                    y_p = 320 + i*35 + scroll_y
                    if y_p > 310:
                        pygame.draw.rect(ventana, (35, 37, 45), (50, y_p, 700, 30), border_radius=5)
                        ventana.blit(f_txt.render(f"ID: {p['id']} - Fecha: {p['fecha']}", True, (200, 200, 200)), (70, y_p + 5))

        dibujar_barra_guia(ventana, guia_actual, f_txt)
        pygame.display.flip()
        reloj.tick(30)
    return "MENU"