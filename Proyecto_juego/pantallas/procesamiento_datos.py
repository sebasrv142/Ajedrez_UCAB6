import struct
import os
import globales as gb

def limpiar_total(dato):
    if isinstance(dato, bytes):
        try:
            dato = dato.decode('utf-8', errors='ignore')
        except:
            dato = str(dato)
    return "".join(char for char in dato if char.isprintable()).strip('\x00').strip()

def obtener_solo_numeros(texto):
    return "".join(filter(str.isdigit, str(texto)))

def formatear_cedula_con_puntos(cedula):
    num = obtener_solo_numeros(cedula)
    res = cedula
    if num:
        res = "{:,}".format(int(num)).replace(",", ".")
    return res

def quicksort(lista, llave):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    izq = [x for x in lista if x[llave] > pivote[llave]]
    centro = [x for x in lista if x[llave] == pivote[llave]]
    der = [x for x in lista if x[llave] < pivote[llave]]
    return quicksort(izq, llave) + centro + quicksort(der, llave)

def obtener_datos_reporte_a():
    """Ranking: Cruza datos y fuerza 0 pts si no existen partidas reales."""
    conteo_juegos = {}
    
    # 1. ESCANEO DE PARTIDAS REALES
    if os.path.exists(gb.ARCHIVO_JUEGOS):
        f_j = open(gb.ARCHIVO_JUEGOS, "rb")
        bloque_j = f_j.read(gb.CANTIDAD_BYTES_JUEGO)
        while bloque_j and len(bloque_j) == gb.CANTIDAD_BYTES_JUEGO:
            dj = struct.unpack(gb.FORMATO_JUEGO, bloque_j)
            id1 = obtener_solo_numeros(limpiar_total(dj[2]))
            id2 = obtener_solo_numeros(limpiar_total(dj[5]))
            if id1: conteo_juegos[id1] = conteo_juegos.get(id1, 0) + 1
            if id2: conteo_juegos[id2] = conteo_juegos.get(id2, 0) + 1
            bloque_j = f_j.read(gb.CANTIDAD_BYTES_JUEGO)
        f_j.close()

    # 2. CARGA DE USUARIOS CON VALIDACIÓN DE ACTIVIDAD
    lista = []
    if os.path.exists(gb.ARCHIVO_USUARIOS):
        f_u = open(gb.ARCHIVO_USUARIOS, "rb")
        bloque_u = f_u.read(gb.CANTIDAD_BYTES_REGISTRO)
        while bloque_u and len(bloque_u) == gb.CANTIDAD_BYTES_REGISTRO:
            d = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_u)
            ced_limpia = obtener_solo_numeros(limpiar_total(d[0]))
            
            # DETERMINAR PARTIDAS
            total_partidas = conteo_juegos.get(ced_limpia, 0)
            
            # --- LÓGICA DE SEGURIDAD TOTAL ---
            if total_partidas == 0:
                # Si no hay juegos en JUEGO.bin, los puntos SON 0 sí o sí
                pts = 0
            else:
                # Si tiene juegos, leemos los puntos del archivo
                raw_pts = obtener_solo_numeros(limpiar_total(d[5]))
                pts = int(raw_pts) if raw_pts else 0
            # ---------------------------------

            lista.append({
                "ced": formatear_cedula_con_puntos(ced_limpia),
                "nom": limpiar_total(d[1]),
                "part": total_partidas,
                "puntos": pts
            })
            bloque_u = f_u.read(gb.CANTIDAD_BYTES_REGISTRO)
        f_u.close()
    
    return quicksort(lista, "puntos")

def buscar_jugador_b(cedula_input):
    """Busca jugador integrando la misma lógica de seguridad sin errores de variables."""
    ced_busqueda = obtener_solo_numeros(cedula_input)
    jugador = None
    juegos = []
    
    # 1. Buscamos historial primero para validar puntos
    if os.path.exists(gb.ARCHIVO_JUEGOS):
        f_h = open(gb.ARCHIVO_JUEGOS, "rb")
        bloque_h = f_h.read(gb.CANTIDAD_BYTES_JUEGO)
        while bloque_h and len(bloque_h) == gb.CANTIDAD_BYTES_JUEGO:
            dj = struct.unpack(gb.FORMATO_JUEGO, bloque_h)
            id_b = obtener_solo_numeros(limpiar_total(dj[2]))
            id_n = obtener_solo_numeros(limpiar_total(dj[5]))
            
            if id_b == ced_busqueda or id_n == ced_busqueda:
                juegos.append({"id": dj[0], "fecha": limpiar_total(dj[1])})
            bloque_h = f_h.read(gb.CANTIDAD_BYTES_JUEGO)
        f_h.close()

    # 2. Buscamos los datos del usuario
    if os.path.exists(gb.ARCHIVO_USUARIOS):
        f = open(gb.ARCHIVO_USUARIOS, "rb")
        bloque = f.read(gb.CANTIDAD_BYTES_REGISTRO)
        while bloque and len(bloque) == gb.CANTIDAD_BYTES_REGISTRO:
            d = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque)
            ced_en_archivo = obtener_solo_numeros(limpiar_total(d[0]))
            
            if ced_en_archivo == ced_busqueda:
                # Si no tiene juegos en la lista 'juegos', puntos = 0
                if len(juegos) == 0:
                    pts_final = 0
                else:
                    raw_pts = obtener_solo_numeros(limpiar_total(d[5]))
                    pts_final = int(raw_pts) if raw_pts else 0
                
                jugador = {
                    "ced": formatear_cedula_con_puntos(ced_en_archivo),
                    "nom": limpiar_total(d[1]),
                    "sex": "Masculino" if "M" in limpiar_total(d[2]).upper() else "Femenino",
                    "fec": limpiar_total(d[3]),
                    "pts": pts_final
                }
            bloque = f.read(gb.CANTIDAD_BYTES_REGISTRO)
        f.close()
        
    return jugador, juegos