def h_condenadas(problema, estado):
    """Heurística h1: número de víctimas vivas que ya no pueden salvarse.

    Una víctima está condenada si su distancia Manhattan al agente supera
    el tiempo que le queda. Manhattan es una cota inferior de la distancia real
    (con paredes se camina más, nunca menos), así que si Manhattan ya no alcanza,
    nada alcanza.
    """
    fila, col, vivas, _, tick = estado
    condenadas = 0
    for vid in vivas:
        v = problema.victimas[vid]
        distancia = abs(fila - v.fila) + abs(col - v.columna)
        if distancia > v.ticks - tick:
            condenadas += 1
    return condenadas