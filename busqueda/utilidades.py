def es_mejor(estado, mejor):
    """Compara un estado objetivo con el mejor nodo encontrado hasta ahora.

    Gana el que tenga más víctimas rescatadas; en empate, el que use menos ticks.
    Si hay empate total se conserva el primero encontrado.
    """
    if mejor is None:
        return True
    rescatadas, ticks = len(estado[3]), estado[4]
    mejor_rescatadas, mejor_ticks = len(mejor.estado[3]), mejor.estado[4]
    return (rescatadas, -ticks) > (mejor_rescatadas, -mejor_ticks)