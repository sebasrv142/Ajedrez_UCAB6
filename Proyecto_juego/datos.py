import globales as gb
import struct
from datetime import datetime

def obtener_nombre_jugador(cedula_a_buscar):
    """
    Busca el nombre de un jugador por su cédula para mostrarlo en la partida.
    """
    nombre_encontrado = "Desconocido"
    # Limpiamos la cédula para asegurar la comparación
    ced_buscada_limpia = str(cedula_a_buscar).replace(".", "").replace("-", "").strip()
    
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as archivo_binario:
            while True:
                bloque_registro = archivo_binario.read(gb.CANTIDAD_BYTES_REGISTRO)
                if not bloque_registro:
                    break
                
                datos_desempaquetados = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_registro)
                cedula_en_archivo = datos_desempaquetados[0].decode('utf-8').strip('\x00').strip()
                ced_archivo_limpia = cedula_en_archivo.replace(".", "").replace("-", "")
                
                if ced_archivo_limpia == ced_buscada_limpia:
                    nombre_encontrado = datos_desempaquetados[1].decode('utf-8').strip('\x00').strip()
                    break
    except:
        pass
    return nombre_encontrado

def actualizar_puntos_jugador(cedula_del_jugador, puntos_para_sumar):
    """
    Busca al jugador y acumula sus puntos en el archivo de usuarios.
    """
    if not cedula_del_jugador or cedula_del_jugador == "Invitado":
        return

    lista_de_registros = []
    usuario_encontrado = False
    ced_buscada_limpia = str(cedula_del_jugador).replace(".", "").replace("-", "").strip()
    
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as archivo_lectura:
            while True:
                bloque_actual = archivo_lectura.read(gb.CANTIDAD_BYTES_REGISTRO)
                if not bloque_actual:
                    break
                
                datos_usuario = list(struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_actual))
                cedula_actual = datos_usuario[0].decode('utf-8').strip('\x00').strip()
                ced_actual_limpia = cedula_actual.replace(".", "").replace("-", "")
                
                if ced_actual_limpia == ced_buscada_limpia:
                    # El campo de puntos es el índice 5
                    cadena_puntos_actuales = datos_usuario[5].decode('utf-8').strip('\x00').strip()
                    valor_puntos_actuales = int(cadena_puntos_actuales) if cadena_puntos_actuales.isdigit() else 0
                    
                    total_puntos_nuevos = valor_puntos_actuales + puntos_para_sumar
                    # Re-empaquetamos los puntos con el largo correcto (40 bytes según tu lógica)
                    datos_usuario[5] = str(total_puntos_nuevos).encode('utf-8').ljust(40, b'\x00')
                    usuario_encontrado = True
                
                lista_de_registros.append(struct.pack(gb.FORMATO_ESTRUCTURA_USUARIO, *datos_usuario))
        
        if usuario_encontrado:
            with open(gb.ARCHIVO_USUARIOS, "wb") as archivo_escritura:
                for registro in lista_de_registros:
                    archivo_escritura.write(registro)
    except Exception as e:
        print(f"Error al actualizar puntos: {e}")

def obtener_catalogo_piezas(es_blanco):
    if es_blanco:
        return gb.PIEZAS_BLANCAS
    return gb.PIEZAS_NEGRAS

def obtener_id_consecutivo_juego():
    identificador_actual = 1
    try:
        with open(gb.ARCHIVO_JUEGOS, "rb") as archivo_juegos:
            while True:
                bloque = archivo_juegos.read(gb.CANTIDAD_BYTES_JUEGO)
                if not bloque: break
                identificador_actual += 1
    except:
        pass
    return identificador_actual

def registrar_juego_binario(pos_inicial_j1, ficha_j1, pos_inicial_j2, ficha_j2):
    id_nuevo_juego = obtener_id_consecutivo_juego()
    fecha_actual_texto = datetime.now().strftime("%d/%m/%Y")
    registro_empaquetado = struct.pack(
        gb.FORMATO_REGISTRO_JUEGO,
        id_nuevo_juego,
        fecha_actual_texto.encode('utf-8'),
        gb.ID_SESION_JUGADOR_UNO.encode('utf-8'),
        ficha_j1.encode('utf-8'),
        pos_inicial_j1.encode('utf-8'),
        gb.ID_SESION_JUGADOR_DOS.encode('utf-8'),
        ficha_j2.encode('utf-8'),
        pos_inicial_j2.encode('utf-8')
    )
    with open(gb.ARCHIVO_JUEGOS, "ab") as archivo_append:
        archivo_append.write(registro_empaquetado)
    return id_nuevo_juego

def registrar_movimiento_binario(id_del_juego, ficha_utilizada, destino_texto, puntos_obtenidos, cedula_jugador):
    """
    Guarda cada movimiento. 
    IMPORTANTE: La cédula se guarda en la posición dm[4] para los reportes.
    """
    fecha_texto = datetime.now().strftime("%d/%m/%Y")
    
    # Formato: i 2s 10s 8s 10s i
    movimiento_empaquetado = struct.pack(
        gb.FORMATO_MOVIMIENTO,
        id_del_juego,                   # dm[0]
        ficha_utilizada.encode('utf-8'),# dm[1]
        fecha_texto.encode('utf-8'),    # dm[2]
        destino_texto.encode('utf-8'),  # dm[3]
        str(cedula_jugador).encode('utf-8'), # dm[4] <- CEDULA
        puntos_obtenidos                # dm[5]
    )
    
    with open(gb.ARCHIVO_MOVIMIENTOS, "ab") as archivo_movs:
        archivo_movs.write(movimiento_empaquetado)
    
    if puntos_obtenidos > 0:
        actualizar_puntos_jugador(cedula_jugador, puntos_obtenidos)