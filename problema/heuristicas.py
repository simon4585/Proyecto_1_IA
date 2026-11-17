def contar_victimas_condenadas(problema, estado):
    """Heurística: número de víctimas vivas que ya no pueden salvarse.

    Una víctima está condenada si su distancia Manhattan al agente es mayor que
    los ticks que le quedan. Manhattan nunca es mayor que la distancia real
    (las paredes solo alargan el camino), así que si Manhattan ya no alcanza,
    ningún camino alcanza. Por eso nunca sobreestima las muertes futuras
    y la heurística es admisible.
    """
    condenadas = 0
    for identificador in estado.vivas:
        victima = problema.victimas[identificador]
        distancia = abs(estado.fila - victima.fila) + abs(estado.columna - victima.columna)
        ticks_restantes = victima.ticks_supervivencia - estado.tick
        if distancia > ticks_restantes:
            condenadas += 1
    return condenadas