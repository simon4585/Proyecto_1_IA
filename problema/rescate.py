# Dirección -> (delta_fila, delta_columna)
DIRECCIONES = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}


class ProblemaRescate:
    """Define el problema de búsqueda.

    Un estado es la tupla: (fila, columna, vivas, rescatadas, tick)
      vivas, rescatadas: frozenset de ids de víctimas
    """

    def __init__(self, mapa, victimas):
        self.mapa = mapa
        self.victimas = {v.id: v for v in victimas}   # id -> Victima
        self.t_max = max(v.ticks for v in victimas)

    def estado_inicial(self):
        f, c = self.mapa.inicio
        return (f, c, frozenset(self.victimas), frozenset(), 0)

    def acciones(self, estado):
        """Lista de (accion, estado_sucesor). No incluye movimientos a paredes."""
        fila, col, _, _, _ = estado
        sucesores = []
        for nombre, (df, dc) in DIRECCIONES.items():
            if self.mapa.es_transitable(fila + df, col + dc):
                sucesores.append((nombre, self.resultado(estado, nombre)))
        return sucesores

    def resultado(self, estado, accion):
        """Aplica una acción: mueve, avanza el tick, rescata y mata víctimas."""
        fila, col, vivas, rescatadas, tick = estado
        df, dc = DIRECCIONES[accion]
        nueva_fila, nueva_col = fila + df, col + dc
        nuevo_tick = tick + 1

        nuevas_vivas = set(vivas)
        nuevas_rescatadas = set(rescatadas)

        # 1) Rescate: el agente pisa la celda de una víctima viva a tiempo
        for vid in vivas:
            v = self.victimas[vid]
            if (v.fila, v.columna) == (nueva_fila, nueva_col) and nuevo_tick <= v.ticks:
                nuevas_vivas.discard(vid)
                nuevas_rescatadas.add(vid)

        # 2) Muerte: las que siguen vivas y cuyo tiempo ya fue superado
        for vid in list(nuevas_vivas):
            if self.victimas[vid].ticks < nuevo_tick:
                nuevas_vivas.discard(vid)

        return (nueva_fila, nueva_col,
                frozenset(nuevas_vivas), frozenset(nuevas_rescatadas), nuevo_tick)

    def es_objetivo(self, estado):
        """Meta: ninguna víctima viva es alcanzable (cota optimista con Manhattan)."""
        fila, col, vivas, _, tick = estado
        for vid in vivas:
            v = self.victimas[vid]
            distancia = abs(fila - v.fila) + abs(col - v.columna)
            if distancia <= v.ticks - tick:
                return False
        return True

    def costo_paso(self, estado, sucesor):
        """Costo = número de víctimas que mueren en esta transición."""
        _, _, vivas, rescatadas, _ = estado
        _, _, nuevas_vivas, nuevas_rescatadas, _ = sucesor
        rescatadas_nuevas = len(nuevas_rescatadas) - len(rescatadas)
        return len(vivas) - len(nuevas_vivas) - rescatadas_nuevas