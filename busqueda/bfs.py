import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda
from busqueda.utilidades import es_mejor_solucion


def bfs(problema):
    """Búsqueda en amplitud sobre todo el espacio de estados.

    La frontera es una lista que se lee con un índice: los nodos se agregan al
    final y se sacan desde el principio, igual que una cola (FIFO).
    """
    tiempo_inicio = time.perf_counter()

    raiz = Nodo(problema.estado_inicial())
    frontera = [raiz]
    indice_siguiente = 0            # posición del siguiente nodo a expandir
    visitados = {raiz.estado}
    nodos_expandidos = 0
    mejor_nodo = None

    while indice_siguiente < len(frontera):
        nodo = frontera[indice_siguiente]
        indice_siguiente += 1

        if problema.es_objetivo(nodo.estado):
            if es_mejor_solucion(nodo.estado, mejor_nodo):
                mejor_nodo = nodo
            continue                # un objetivo no se expande más

        nodos_expandidos += 1
        for accion, sucesor in problema.acciones(nodo.estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                costo = nodo.costo + problema.costo_paso(nodo.estado, sucesor)
                frontera.append(Nodo(sucesor, nodo, accion, costo))

    tiempo_total = time.perf_counter() - tiempo_inicio
    return ResultadoBusqueda("BFS", mejor_nodo, nodos_expandidos, tiempo_total)