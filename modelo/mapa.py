class Mapa:
    """Cuadrícula del entorno. Solo '#' es pared; cualquier otro símbolo es transitable."""

    def __init__(self, cuadricula, inicio):
        self.cuadricula = cuadricula          # lista de strings, una por fila
        self.inicio = inicio                  # (fila, columna) de 'S'
        self.filas = len(cuadricula)
        self.columnas = len(cuadricula[0])

    @classmethod
    def desde_lineas(cls, lineas):
        """Construye el mapa desde las líneas de mapa.txt y localiza 'S'."""
        cuadricula = [l.rstrip("\n") for l in lineas if l.strip()]
        if len({len(f) for f in cuadricula}) != 1:
            raise ValueError("Todas las filas del mapa deben tener el mismo largo")
        inicio = None
        for f, fila in enumerate(cuadricula):
            if "S" in fila:
                inicio = (f, fila.index("S"))
        if inicio is None:
            raise ValueError("El mapa no tiene posición inicial 'S'")
        return cls(cuadricula, inicio)

    def es_transitable(self, fila, columna):
        """False si está fuera del mapa o es pared."""
        return (0 <= fila < self.filas
                and 0 <= columna < self.columnas
                and self.cuadricula[fila][columna] != "#")