from modelo.mapa import Mapa
from modelo.victima import Victima

CARACTERES_VALIDOS = set("#.SV0123456789")


class ErrorDeArchivo(Exception):
    """Archivo de entrada ilegible o con formato inválido (mensaje apto para mostrar)."""


def _leer_lineas(ruta):
    """Devuelve las líneas del archivo sin saltos de línea."""
    try:
        with open(ruta, encoding="utf-8-sig") as archivo:
            return archivo.read().splitlines()
    except OSError as error:
        raise ErrorDeArchivo(f"No se pudo abrir '{ruta}': {error.strerror}")
    except UnicodeDecodeError:
        raise ErrorDeArchivo(f"'{ruta}' no es un archivo de texto UTF-8 válido")


def cargar_mapa(ruta):
    """Lee mapa.txt y devuelve un Mapa. Lanza ErrorDeArchivo si el formato es inválido."""
    lineas = [l.rstrip() for l in _leer_lineas(ruta) if l.strip()]
    if not lineas:
        raise ErrorDeArchivo("El archivo del mapa está vacío")

    ancho = len(lineas[0])
    posiciones_s = []
    for f, linea in enumerate(lineas):
        if len(linea) != ancho:
            raise ErrorDeArchivo(
                f"Mapa: la fila {f + 1} mide {len(linea)} y la primera mide {ancho}")
        for c, caracter in enumerate(linea):
            if caracter not in CARACTERES_VALIDOS:
                raise ErrorDeArchivo(
                    f"Mapa: carácter no válido '{caracter}' en fila {f + 1}, columna {c + 1}")
            if caracter == "S":
                posiciones_s.append((f, c))

    if len(posiciones_s) == 0:
        raise ErrorDeArchivo("Mapa: no hay posición inicial 'S'")
    if len(posiciones_s) > 1:
        raise ErrorDeArchivo("Mapa: hay más de una 'S'")

    return Mapa.desde_lineas(lineas)


def cargar_victimas(ruta, mapa):
    """Lee victimas.txt. Devuelve (lista_de_Victima, lista_de_advertencias)."""
    victimas = []
    advertencias = []
    ids_vistos = set()
    primera_linea = True

    for numero, linea in enumerate(_leer_lineas(ruta), start=1):
        if not linea.strip():
            continue
        partes = [p.strip() for p in linea.split(",")]
        if len(partes) != 4:
            raise ErrorDeArchivo(
                f"Víctimas, línea {numero}: se esperaban 4 campos y hay {len(partes)}")

        try:
            fila, columna, ticks = int(partes[1]), int(partes[2]), int(partes[3])
        except ValueError:
            if primera_linea:           # cabecera: id,fila,columna,ticks_supervivencia
                primera_linea = False
                continue
            raise ErrorDeArchivo(f"Víctimas, línea {numero}: fila, columna y ticks deben ser enteros")
        primera_linea = False

        identificador = partes[0]
        if not identificador:
            raise ErrorDeArchivo(f"Víctimas, línea {numero}: falta el id")
        if identificador in ids_vistos:
            raise ErrorDeArchivo(f"Víctimas, línea {numero}: el id '{identificador}' está repetido")
        if ticks <= 0:
            raise ErrorDeArchivo(f"Víctimas, línea {numero}: los ticks deben ser mayores que 0")
        if not (0 <= fila < mapa.filas and 0 <= columna < mapa.columnas):
            raise ErrorDeArchivo(
                f"Víctimas, línea {numero}: {identificador} está fuera del mapa ({fila},{columna})")
        if not mapa.es_transitable(fila, columna):
            advertencias.append(
                f"{identificador} está en ({fila},{columna}), que es pared: no se puede rescatar")

        ids_vistos.add(identificador)
        victimas.append(Victima(identificador, fila, columna, ticks))

    if not victimas:
        raise ErrorDeArchivo("El archivo de víctimas no contiene ninguna víctima")
    return victimas, advertencias