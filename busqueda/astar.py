import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda
from busqueda.utilidades import es_mejor_solucion
from problema.heuristicas import contar_victimas_condenadas


def astar(problema, heuristica=contar_victimas_condenadas):
    """Búsqueda A*: expande primero el nodo con menor f = costo + heurística.

    costo = muertes acumuladas, heurística = víctimas ya condenadas.
    La frontera es una lista de tuplas (f, tick, contador, nodo).
    """
    tiempo_inicio = time.perf_counter()
    total_victimas = len(problema.victimas)

    raiz = Nodo(problema.estado_inicial())
    contador = 0
    f_raiz = heuristica(problema, raiz.estado)      # costo 0 + heurística
    frontera = [(f_raiz, 0, contador, raiz)]
    visitados = {raiz.estado}
    nodos_expandidos = 0
    mejor_nodo = None
    muertes_del_mejor = total_victimas + 1

    while len(frontera) > 0:
        elegido = min(frontera)
        frontera.remove(elegido)
        f_elegido, tick_elegido, orden, nodo = elegido

        # Ningún nodo restante puede mejorar al mejor objetivo ya encontrado
        if f_elegido > muertes_del_mejor:
            break

        if problema.es_objetivo(nodo.estado):
            if es_mejor_solucion(nodo.estado, mejor_nodo):
                mejor_nodo = nodo
                muertes_del_mejor = total_victimas - len(nodo.estado.rescatadas)
            continue

        nodos_expandidos += 1
        for accion, sucesor in problema.acciones(nodo.estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                costo = nodo.costo + problema.costo_paso(nodo.estado, sucesor)
                f_hijo = costo + heuristica(problema, sucesor)
                contador += 1
                hijo = Nodo(sucesor, nodo, accion, costo)
                frontera.append((f_hijo, sucesor.tick, contador, hijo))

    tiempo_total = time.perf_counter() - tiempo_inicio
    return ResultadoBusqueda("A*", mejor_nodo, nodos_expandidos, tiempo_total)