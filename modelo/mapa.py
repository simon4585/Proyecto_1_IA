class Mapa:
    """Cuadrícula del entorno. Solo '#' es pared; cualquier otro símbolo se puede pisar."""

    def __init__(self, cuadricula):
        self.cuadricula = cuadricula          # lista de textos, uno por fila
        self.filas = len(cuadricula)
        self.columnas = len(cuadricula[0])
        self.inicio = self.buscar_inicio()    # (fila, columna) donde está la 'S'

    def buscar_inicio(self):
        """Recorre el mapa hasta encontrar la letra 'S'."""
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.cuadricula[fila][columna] == "S":
                    return (fila, columna)
        return None

    def es_transitable(self, fila, columna):
        """False si la posición está fuera del mapa o es una pared."""
        if fila < 0 or fila >= self.filas:
            return False
        if columna < 0 or columna >= self.columnas:
            return False
        return self.cuadricula[fila][columna] != "#"