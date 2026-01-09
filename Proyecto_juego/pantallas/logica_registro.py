import struct
import globales as gb

def validar_reglas_seguridad_clave(clave_texto, posicion_caracter=0, tiene_mayuscula=False, tiene_minuscula=False, tiene_numero=False, tiene_especial=False, contador_numeros=0):
    caracteres_especiales_validos = ["*", "=", "%", "_"]
    longitud_clave = len(clave_texto)
    
    if longitud_clave < 6 or longitud_clave > 10:
        return False, "Debe tener 6-10 caracteres."
        
    if posicion_caracter == longitud_clave:
        errores_encontrados = []
        if not tiene_mayuscula: errores_encontrados.append("mayúscula")
        if not tiene_minuscula: errores_encontrados.append("minúscula")
        if not tiene_numero:    errores_encontrados.append("número")
        if not tiene_especial:  errores_encontrados.append("especial")
        
        resultado = (True, "") if len(errores_encontrados) == 0 else (False, "Falta: " + ", ".join(errores_encontrados))
        return resultado
    
    caracter_actual = clave_texto[posicion_caracter]
    if 'A' <= caracter_actual <= 'Z': tiene_mayuscula = True
    elif 'a' <= caracter_actual <= 'z': tiene_minuscula = True
    elif caracter_actual.isdigit():
        tiene_numero = True
        contador_numeros += 1
        # MEJORA: Validación recursiva para limitar la cantidad exacta de números permitidos
        if contador_numeros > 3: return False, "Máximo 3 números."
    elif caracter_actual in caracteres_especiales_validos: tiene_especial = True
    else: return False, f"Carácter '{caracter_actual}' no permitido."
    
    return validar_reglas_seguridad_clave(clave_texto, posicion_caracter + 1, tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial, contador_numeros)

def transformar_clave_a_encriptada(clave_original):
    resultado_encriptado = ""
    for unidad_caracter in clave_original:
        resultado_encriptado += chr(ord(unidad_caracter) + 2)
    return resultado_encriptado

def comprobar_si_usuario_existe(cedula_a_buscar):
    usuario_encontrado = False
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as archivo_binario:
            bloque_datos = archivo_binario.read(gb.CANTIDAD_BYTES_REGISTRO)
            # MEJORA: Uso de bandera 'usuario_encontrado' para evitar el uso de 'break' en archivos binarios
            while bloque_datos and not usuario_encontrado:
                datos_desempaquetados = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_datos)
                cedula_en_archivo = datos_desempaquetados[0].decode('utf-8').replace('\x00', '').strip()
                if cedula_en_archivo == cedula_a_buscar.strip():
                    usuario_encontrado = True
                else:
                    bloque_datos = archivo_binario.read(gb.CANTIDAD_BYTES_REGISTRO)
    except FileNotFoundError: pass
    return usuario_encontrado

def validar_campo_actual(indice_campo, valor_campo):
    if not valor_campo.strip(): return False, "No puede estar vacío."
    
    if indice_campo == 0:
        # MEJORA: Verificación de duplicados en tiempo real antes de permitir avanzar
        if comprobar_si_usuario_existe(valor_campo): return False, "Cédula ya registrada."
    
    elif indice_campo == 1:
        if len(valor_campo) < 4: return False, "Mínimo 4 caracteres."
    
    elif indice_campo == 2:
        if valor_campo.lower() not in ['m', 'f']: return False, "Use 'M' o 'F'."
    
    elif indice_campo == 3:
        partes_fecha = valor_campo.split("/")
        if len(partes_fecha) != 3: return False, "Use DD/MM/AAAA."
        try:
            dia, mes, anio = int(partes_fecha[0]), int(partes_fecha[1]), int(partes_fecha[2])
            if dia < 1 or dia > 31: return False, "Día inválido (1-31)."
            if mes < 1 or mes > 12: return False, "Mes inválido (1-12)."
            # MEJORA: Restricción de fecha actualizada al contexto del año actual (2026)
            if anio > 2026: return False, "El año no puede ser mayor a 2026."
        except ValueError: return False, "Fecha debe ser numérica."
    
    elif indice_campo == 4:
        # MEJORA: Validación estricta de dominios permitidos (Gmail/Hotmail)
        if "@" not in valor_campo: return False, "Falta el '@'."
        if not (valor_campo.lower().endswith("gmail.com") or valor_campo.lower().endswith("hotmail.com")):
            return False, "Debe ser gmail o hotmail."
            
    elif indice_campo == 5:
        return validar_reglas_seguridad_clave(valor_campo)
        
    return True, ""