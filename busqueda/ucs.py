import time

from busqueda.nodo import Nodo
from busqueda.resultado import ResultadoBusqueda
from busqueda.utilidades import es_mejor


def ucs(problema):
    """Búsqueda de costo uniforme: expande primero el nodo con menos muertes acumuladas.

    La frontera es una lista de tuplas:
        (costo g, tick, contador, nodo)
    En cada paso se extrae la tupla más pequeña con min(). El contador es único,
    así que nunca se llega a comparar dos Nodo, y conserva el orden de generación
    (izquierda a derecha) cuando hay empates.
    """
    inicio = time.perf_counter()
    total = len(problema.victimas)

    raiz = Nodo(problema.estado_inicial())
    contador = 0
    frontera = [(0, 0, contador, raiz)]
    visitados = {raiz.estado}
    expandidos = 0
    mejor = None
    muertes_mejor = total + 1          # muertes del mejor objetivo encontrado

    while frontera:
        elegido = min(frontera)        # tupla de menor costo (luego menor tick, luego orden)
        frontera.remove(elegido)
        g, _, _, nodo = elegido

        # Ningún nodo restante puede mejorar al mejor objetivo ya encontrado
        if g > muertes_mejor:
            break

        if problema.es_objetivo(nodo.estado):
            if es_mejor(nodo.estado, mejor):
                mejor = nodo
                muertes_mejor = total - len(nodo.estado[3])   # costo real del objetivo
            continue                    # un objetivo no se expande más

        expandidos += 1
        for accion, sucesor in problema.acciones(nodo.estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                costo = nodo.costo + problema.costo_paso(nodo.estado, sucesor)
                contador += 1
                hijo = Nodo(sucesor, nodo, accion, costo)
                frontera.append((costo, sucesor[4], contador, hijo))

    return ResultadoBusqueda("UCS", mejor, expandidos, time.perf_counter() - inicio)