class ResultadoBusqueda:
    """Lo que devuelve cualquier algoritmo de búsqueda (BFS, UCS, IDDFS, A*)."""

    def __init__(self, algoritmo, nodo_meta, nodos_expandidos, tiempo):
        self.algoritmo = algoritmo                  # nombre: "BFS", "UCS", ...
        self.nodo_meta = nodo_meta                  # Nodo objetivo elegido (o None)
        self.nodos_expandidos = nodos_expandidos    # nodos de los que se generaron sucesores
        self.tiempo = tiempo                        # segundos

        if nodo_meta is not None:
            self.camino = nodo_meta.camino()                # lista de estados, de inicio a meta
            self.acciones = nodo_meta.acciones()            # lista de 'N', 'S', 'E', 'O'
            self.rescatadas = len(nodo_meta.estado[3])      # estado[3] = frozenset de rescatadas
            self.ticks = nodo_meta.estado[4]                # estado[4] = tick final
        else:
            # La búsqueda no encontró ningún estado objetivo
            self.camino = []
            self.acciones = []
            self.rescatadas = 0
            self.ticks = 0