import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda
from busqueda.utilidades import es_mejor_solucion


class BusquedaProfundidadLimitada:
    """Una pasada de DFS que no baja más allá de un límite de profundidad.

    La profundidad de un nodo es su tick (cada movimiento suma 1 tick).
    Guarda el mejor objetivo y la cantidad de nodos expandidos, y se reutiliza
    en todas las pasadas de IDDFS.
    """

    def __init__(self, problema):
        self.problema = problema
        self.nodos_expandidos = 0
        self.mejor_nodo = None
        self.limite = 0
        self.visitados = set()

    def explorar_con_limite(self, limite):
        """Hace una pasada completa. Devuelve True si el límite cortó alguna rama."""
        self.limite = limite
        estado_inicial = self.problema.estado_inicial()
        self.visitados = {estado_inicial}       # se reinicia en cada pasada
        return self.explorar(Nodo(estado_inicial))

    def explorar(self, nodo):
        """DFS recursiva. Devuelve True si alguna rama quedó cortada por el límite."""
        if self.problema.es_objetivo(nodo.estado):
            if es_mejor_solucion(nodo.estado, self.mejor_nodo):
                self.mejor_nodo = nodo
            return False                        # un objetivo no se expande más

        if nodo.estado.tick >= self.limite:
            return True                         # se llegó al límite: queda por explorar

        self.nodos_expandidos += 1
        hubo_corte = False
        for accion, sucesor in self.problema.acciones(nodo.estado):
            if sucesor not in self.visitados:
                self.visitados.add(sucesor)
                costo = nodo.costo + self.problema.costo_paso(nodo.estado, sucesor)
                hijo = Nodo(sucesor, nodo, accion, costo)
                if self.explorar(hijo):
                    hubo_corte = True
        return hubo_corte


def iddfs(problema):
    """Búsqueda en profundidad iterativa.

    Repite la DFS con límite 0, 1, 2, ... hasta que una pasada recorra todo el
    espacio sin cortes. Conserva el mejor objetivo encontrado en todas las pasadas.
    """
    tiempo_inicio = time.perf_counter()
    busqueda = BusquedaProfundidadLimitada(problema)

    limite = 0
    while True:
        hubo_corte = busqueda.explorar_con_limite(limite)
        if not hubo_corte:
            break                               # se exploró todo el espacio
        limite += 1

    tiempo_total = time.perf_counter() - tiempo_inicio
    return ResultadoBusqueda("IDDFS", busqueda.mejor_nodo,
                             busqueda.nodos_expandidos, tiempo_total)