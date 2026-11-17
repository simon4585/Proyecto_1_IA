class Nodo:
    """Nodo del árbol de búsqueda: un estado y cómo se llegó a él."""

    def __init__(self, estado, padre=None, accion=None, costo=0):
        self.estado = estado      # Estado (fila, columna, vivas, rescatadas, tick)
        self.padre = padre        # Nodo anterior (None en la raíz)
        self.accion = accion      # 'N', 'S', 'E' u 'O'
        self.costo = costo        # muertes acumuladas hasta este nodo

    def camino(self):
        """Lista de estados desde la raíz hasta este nodo."""
        estados = []
        nodo = self
        while nodo is not None:
            estados.append(nodo.estado)
            nodo = nodo.padre
        estados.reverse()
        return estados

    def acciones(self):
        """Lista de acciones desde la raíz hasta este nodo."""
        lista_de_acciones = []
        nodo = self
        while nodo.padre is not None:
            lista_de_acciones.append(nodo.accion)
            nodo = nodo.padre
        lista_de_acciones.reverse()
        return lista_de_acciones