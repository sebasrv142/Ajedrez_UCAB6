import struct
import os
import pygame

# --- CONFIGURACIÓN DE RUTAS ---
NOMBRE_CARPETA = "archivos_sistema"
if not os.path.exists(NOMBRE_CARPETA):
    os.makedirs(NOMBRE_CARPETA)

# --- CONFIGURACIÓN BINARIA ---
# Prefijo '<' para lectura Little-endian
FORMATO_ESTRUCTURA_USUARIO = "<10s30s1s10s15s40s"
CANTIDAD_BYTES_REGISTRO = struct.calcsize(FORMATO_ESTRUCTURA_USUARIO)
ARCHIVO_USUARIOS = os.path.join(NOMBRE_CARPETA, "JUGADORES.bin")

ARCHIVO_JUEGOS = os.path.join(NOMBRE_CARPETA, "JUEGO.bin")
FORMATO_JUEGO = "<i10s15s2s5s15s2s5s"
CANTIDAD_BYTES_JUEGO = struct.calcsize(FORMATO_JUEGO)

# Ajuste en formato movimiento para asegurar integridad de datos
ARCHIVO_MOVIMIENTOS = os.path.join(NOMBRE_CARPETA, "MOVIMIENTOS.bin")
FORMATO_MOVIMIENTO = "<i2s10s8s10si" 
CANTIDAD_BYTES_MOVIMIENTO = struct.calcsize(FORMATO_MOVIMIENTO)

# --- CONFIGURACIÓN VISUAL ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
COLOR_FONDO = (30, 32, 40)      # Fondo oscuro para consistencia con reportes
COLOR_TEXTO = (255, 255, 255)
COLOR_SELECCION = (212, 175, 55) # Dorado
COLOR_TABLERO_CLARO = (238, 238, 210)
COLOR_TABLERO_OSCURO = (118, 150, 86)

# --- VARIABLES DE ESTADO Y LÓGICA ---
ID_SESION_JUGADOR_UNO = ""
ID_SESION_JUGADOR_DOS = ""
DIMENSION_TABLERO = 8

# SOLUCIÓN AL ERROR: Constante para celdas vacías
VACIO = 0 

# --- UTILIDADES ---
def cargar_imagen(nombre_archivo, escala=None):
    ruta = os.path.join("assets", nombre_archivo)
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        if escala:
            imagen = pygame.transform.scale(imagen, escala)
        return imagen
    except:
        # Si falla, devuelve un cuadro de color base para no romper el juego
        superficie_error = pygame.Surface(escala if escala else (50, 50))
        superficie_error.fill((200, 0, 0))
        return superficie_error