import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda
from busqueda.utilidades import es_mejor
from problema.heuristicas import h_condenadas


def astar(problema, heuristica=h_condenadas):
    """Búsqueda A*: expande primero el nodo con menor f = g + h.

    g = muertes acumuladas, h = heurística (por defecto, víctimas condenadas).
    La frontera es una lista de tuplas (f, tick, contador, nodo).
    """
    inicio = time.perf_counter()
    total = len(problema.victimas)

    raiz = Nodo(problema.estado_inicial())
    contador = 0
    h_raiz = heuristica(problema, raiz.estado)
    frontera = [(h_raiz, 0, contador, raiz)]      # f = 0 + h
    visitados = {raiz.estado}
    expandidos = 0
    mejor = None
    muertes_mejor = total + 1

    while frontera:
        elegido = min(frontera)
        frontera.remove(elegido)
        f, _, _, nodo = elegido

        # Ningún nodo restante puede mejorar al mejor objetivo ya encontrado
        if f > muertes_mejor:
            break

        if problema.es_objetivo(nodo.estado):
            if es_mejor(nodo.estado, mejor):
                mejor = nodo
                muertes_mejor = total - len(nodo.estado[3])
            continue

        expandidos += 1
        for accion, sucesor in problema.acciones(nodo.estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                costo = nodo.costo + problema.costo_paso(nodo.estado, sucesor)
                f_hijo = costo + heuristica(problema, sucesor)
                contador += 1
                hijo = Nodo(sucesor, nodo, accion, costo)
                frontera.append((f_hijo, sucesor[4], contador, hijo))

    return ResultadoBusqueda("A*", mejor, expandidos, time.perf_counter() - inicio)