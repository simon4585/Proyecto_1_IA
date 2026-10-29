import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda


def _es_mejor(estado, mejor):
    """Compara un estado objetivo con el mejor encontrado hasta ahora.

    Gana el que tenga más víctimas rescatadas; en empate, el que use menos ticks.
    Si hay empate total, se conserva el primero encontrado (el más a la izquierda).
    """
    if mejor is None:
        return True
    rescatadas, ticks = len(estado[3]), estado[4]
    mejor_rescatadas, mejor_ticks = len(mejor.estado[3]), mejor.estado[4]
    return (rescatadas, -ticks) > (mejor_rescatadas, -mejor_ticks)


def bfs(problema):
    """Búsqueda en amplitud sobre todo el espacio de estados (acotado por t_max).

    La frontera es una lista que se recorre con un índice: los nodos se agregan
    al final y se leen desde el principio, igual que una cola FIFO.
    """
    inicio = time.perf_counter()

    raiz = Nodo(problema.estado_inicial())
    frontera = [raiz]
    indice = 0                      # posición del siguiente nodo a expandir
    visitados = {raiz.estado}
    expandidos = 0
    mejor = None

    while indice < len(frontera):
        nodo = frontera[indice]
        indice += 1

        if problema.es_objetivo(nodo.estado):
            if _es_mejor(nodo.estado, mejor):
                mejor = nodo
            continue                # un objetivo no se expande más

        expandidos += 1
        for accion, sucesor in problema.acciones(nodo.estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                costo = nodo.costo + problema.costo_paso(nodo.estado, sucesor)
                frontera.append(Nodo(sucesor, nodo, accion, costo))

    return ResultadoBusqueda("BFS", mejor, expandidos, time.perf_counter() - inicio)