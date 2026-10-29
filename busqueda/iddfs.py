import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda
from busqueda.utilidades import es_mejor


def _dfs_limitada(problema, nodo, limite, visitados, contexto):
    """Búsqueda en profundidad con límite. Devuelve True si hubo nodos cortados por el límite.

    La profundidad de un nodo es su tick (cada movimiento suma 1 tick).
    contexto = {"expandidos": int, "mejor": Nodo}, compartido entre llamadas recursivas.
    """
    if problema.es_objetivo(nodo.estado):
        if es_mejor(nodo.estado, contexto["mejor"]):
            contexto["mejor"] = nodo
        return False                       # un objetivo no se expande más

    if nodo.estado[4] >= limite:
        return True                        # se llegó al límite sin ser objetivo: queda por explorar

    contexto["expandidos"] += 1
    cortado = False
    for accion, sucesor in problema.acciones(nodo.estado):
        if sucesor not in visitados:
            visitados.add(sucesor)
            costo = nodo.costo + problema.costo_paso(nodo.estado, sucesor)
            hijo = Nodo(sucesor, nodo, accion, costo)
            if _dfs_limitada(problema, hijo, limite, visitados, contexto):
                cortado = True
    return cortado


def iddfs(problema):
    """Búsqueda en profundidad iterativa (Iterative Deepening DFS).

    Repite la DFS limitada con límite 0, 1, 2, ... hasta que una iteración
    recorra todo el espacio sin cortes. Conserva el mejor objetivo encontrado.
    """
    inicio = time.perf_counter()
    contexto = {"expandidos": 0, "mejor": None}
    estado_inicial = problema.estado_inicial()

    limite = 0
    while True:
        visitados = {estado_inicial}       # se reinicia en cada iteración
        raiz = Nodo(estado_inicial)
        hubo_cortes = _dfs_limitada(problema, raiz, limite, visitados, contexto)
        if not hubo_cortes:
            break                          # se exploró todo el espacio
        limite += 1

    return ResultadoBusqueda("IDDFS", contexto["mejor"], contexto["expandidos"],
                                time.perf_counter() - inicio)