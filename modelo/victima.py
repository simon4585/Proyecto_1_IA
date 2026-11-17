class Victima:
    """Una víctima: dónde está y cuántos ticks puede sobrevivir."""

    def __init__(self, identificador, fila, columna, ticks_supervivencia):
        self.identificador = identificador              # por ejemplo "V1"
        self.fila = fila
        self.columna = columna
        self.ticks_supervivencia = ticks_supervivencia  # tick máximo en que aún se puede rescatar