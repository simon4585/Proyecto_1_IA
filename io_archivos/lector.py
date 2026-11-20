from modelo.mapa import Mapa
from modelo.victima import Victima

CARACTERES_VALIDOS = set("#.SV0123456789")


class ErrorDeArchivo(Exception):
    """Archivo ilegible o con formato inválido. El mensaje se muestra al usuario."""


def leer_lineas(ruta):
    """Devuelve las líneas del archivo sin los saltos de línea."""
    try:
        with open(ruta, encoding="utf-8-sig") as archivo:
            return archivo.read().splitlines()
    except OSError as error:
        raise ErrorDeArchivo("No se pudo abrir '" + ruta + "': " + str(error.strerror))
    except UnicodeDecodeError:
        raise ErrorDeArchivo("'" + ruta + "' no es un archivo de texto UTF-8 válido")


def cargar_mapa(ruta):
    """Lee mapa.txt, valida su formato y devuelve un Mapa."""
    lineas = []

    for linea in leer_lineas(ruta):
        if linea.strip() != "":
            lineas.append(linea.rstrip())

    if len(lineas) == 0:
        raise ErrorDeArchivo("El archivo del mapa está vacío")

    ancho = len(lineas[0])
    cantidad_de_inicios = 0

    for fila in range(len(lineas)):
        if len(lineas[fila]) != ancho:
            raise ErrorDeArchivo("Mapa: la fila " + str(fila + 1) + " mide "
                                 + str(len(lineas[fila])) + " y la primera mide " + str(ancho))

        for columna in range(ancho):
            caracter = lineas[fila][columna]

            if caracter not in CARACTERES_VALIDOS:
                raise ErrorDeArchivo("Mapa: carácter no válido '" + caracter + "' en la fila "
                                     + str(fila + 1) + ", columna " + str(columna + 1))

            if caracter == "S":
                cantidad_de_inicios += 1

    if cantidad_de_inicios == 0:
        raise ErrorDeArchivo("Mapa: no hay posición inicial 'S'")

    if cantidad_de_inicios > 1:
        raise ErrorDeArchivo("Mapa: hay más de una 'S'")

    return Mapa(lineas)


def cargar_victimas(ruta, mapa):
    """Lee victimas.txt. Devuelve (lista de Victima, lista de advertencias)."""
    victimas = []
    advertencias = []
    identificadores_vistos = set()

    lineas = leer_lineas(ruta)

    for numero in range(1, len(lineas) + 1):
        linea = lineas[numero - 1]

        if linea.strip() == "":
            continue

        partes = []

        for parte in linea.split(","):
            partes.append(parte.strip())

        if len(partes) != 4:
            raise ErrorDeArchivo("Víctimas, línea " + str(numero)
                                 + ": se esperaban 4 campos y hay " + str(len(partes)))

        try:
            fila = int(partes[1])
            columna = int(partes[2])
            ticks_supervivencia = int(partes[3])

        except ValueError:
            if numero == 1:
                continue    # es la cabecera: id,fila,columna,ticks_supervivencia

            raise ErrorDeArchivo("Víctimas, línea " + str(numero)
                                 + ": fila, columna y ticks deben ser enteros")

        identificador = partes[0]

        if identificador == "":
            raise ErrorDeArchivo("Víctimas, línea " + str(numero) + ": falta el id")

        if identificador in identificadores_vistos:
            raise ErrorDeArchivo("Víctimas, línea " + str(numero) + ": el id '"
                                 + identificador + "' está repetido")

        if ticks_supervivencia <= 0:
            raise ErrorDeArchivo("Víctimas, línea " + str(numero)
                                 + ": los ticks deben ser mayores que 0")

        if fila < 0 or fila >= mapa.filas or columna < 0 or columna >= mapa.columnas:
            raise ErrorDeArchivo("Víctimas, línea " + str(numero) + ": " + identificador
                                 + " está fuera del mapa (" + str(fila) + "," + str(columna) + ")")

        if not mapa.es_transitable(fila, columna):
            advertencias.append(identificador + " está en (" + str(fila) + "," + str(columna)
                                + "), que es pared: no se puede rescatar")

        identificadores_vistos.add(identificador)

        victimas.append(Victima(identificador, fila, columna, ticks_supervivencia))

    if len(victimas) == 0:
        raise ErrorDeArchivo("El archivo de víctimas no contiene ninguna víctima")

    return victimas, advertencias