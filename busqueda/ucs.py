import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda
from busqueda.utilidades import es_mejor_solucion


def ucs(problema):
    """Búsqueda de costo uniforme: expande primero el nodo con menos muertes acumuladas.

    La frontera es una lista de tuplas (costo, tick, contador, nodo). En cada paso
    se saca la tupla más pequeña con min(): primero menor costo, luego menor tick,
    y por último el orden de generación. El contador es único, así que nunca se
    llega a comparar dos Nodo entre sí.
    """
    tiempo_inicio = time.perf_counter()
    total_victimas = len(problema.victimas)

    raiz = Nodo(problema.estado_inicial())
    contador = 0
    frontera = [(0, 0, contador, raiz)]
    visitados = {raiz.estado}
    nodos_expandidos = 0
    mejor_nodo = None
    muertes_del_mejor = total_victimas + 1      # muertes del mejor objetivo encontrado

    while len(frontera) > 0:
        elegido = min(frontera)
        frontera.remove(elegido)
        costo_elegido, tick_elegido, orden, nodo = elegido

        # Ningún nodo restante puede mejorar al mejor objetivo ya encontrado
        if costo_elegido > muertes_del_mejor:
            break

        if problema.es_objetivo(nodo.estado):
            if es_mejor_solucion(nodo.estado, mejor_nodo):
                mejor_nodo = nodo
                muertes_del_mejor = total_victimas - len(nodo.estado.rescatadas)
            continue                    # un objetivo no se expande más

        nodos_expandidos += 1
        for accion, sucesor in problema.acciones(nodo.estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                costo = nodo.costo + problema.costo_paso(nodo.estado, sucesor)
                contador += 1
                hijo = Nodo(sucesor, nodo, accion, costo)
                frontera.append((costo, sucesor.tick, contador, hijo))

    tiempo_total = time.perf_counter() - tiempo_inicio
    return ResultadoBusqueda("UCS", mejor_nodo, nodos_expandidos, tiempo_total)