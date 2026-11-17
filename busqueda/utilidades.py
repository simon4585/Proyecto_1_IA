def es_mejor_solucion(estado, mejor_nodo):
    """Compara un estado objetivo con el mejor nodo encontrado hasta ahora.

    Gana el que tenga más víctimas rescatadas; si empatan, el que use menos ticks.
    Si empatan en todo se conserva el primero que se encontró.
    """
    if mejor_nodo is None:
        return True
    rescatadas_nuevo = len(estado.rescatadas)
    rescatadas_mejor = len(mejor_nodo.estado.rescatadas)
    if rescatadas_nuevo != rescatadas_mejor:
        return rescatadas_nuevo > rescatadas_mejor
    return estado.tick < mejor_nodo.estado.tick