from problema.estado import Estado

# Dirección -> (cambio en la fila, cambio en la columna)
DIRECCIONES = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}


class ProblemaRescate:
    """Define el problema de búsqueda: estado inicial, acciones, resultado y meta.

    La búsqueda termina sola porque el tick forma parte del estado: pasado el
    mayor tiempo de supervivencia todas las víctimas están muertas y el estado
    es objetivo.
    """

    def __init__(self, mapa, victimas):
        self.mapa = mapa
        self.victimas = {}                      # identificador -> Victima
        for victima in victimas:
            self.victimas[victima.identificador] = victima

    def estado_inicial(self):
        fila, columna = self.mapa.inicio
        todas_vivas = frozenset(self.victimas)  # los ids de todas las víctimas
        return Estado(fila, columna, todas_vivas, frozenset(), 0)

    def acciones(self, estado):
        """Lista de (nombre de la acción, estado sucesor). No incluye paredes."""
        sucesores = []
        for nombre, (cambio_fila, cambio_columna) in DIRECCIONES.items():
            nueva_fila = estado.fila + cambio_fila
            nueva_columna = estado.columna + cambio_columna
            if self.mapa.es_transitable(nueva_fila, nueva_columna):
                sucesores.append((nombre, self.resultado(estado, nombre)))
        return sucesores

    def resultado(self, estado, accion):
        """Aplica una acción: mueve al agente, suma un tick, rescata y mata víctimas."""
        cambio_fila, cambio_columna = DIRECCIONES[accion]
        nueva_fila = estado.fila + cambio_fila
        nueva_columna = estado.columna + cambio_columna
        nuevo_tick = estado.tick + 1

        nuevas_vivas = set(estado.vivas)
        nuevas_rescatadas = set(estado.rescatadas)

        # 1) Rescate: el agente pisa la celda de una víctima viva a tiempo
        for identificador in estado.vivas:
            victima = self.victimas[identificador]
            esta_en_la_celda = (victima.fila == nueva_fila and victima.columna == nueva_columna)
            if esta_en_la_celda and nuevo_tick <= victima.ticks_supervivencia:
                nuevas_vivas.remove(identificador)
                nuevas_rescatadas.add(identificador)

        # 2) Muerte: las que siguen vivas y cuyo tiempo ya se superó
        for identificador in list(nuevas_vivas):
            if self.victimas[identificador].ticks_supervivencia < nuevo_tick:
                nuevas_vivas.remove(identificador)

        return Estado(nueva_fila, nueva_columna,
                      frozenset(nuevas_vivas), frozenset(nuevas_rescatadas), nuevo_tick)

    def es_objetivo(self, estado):
        """Meta: ninguna víctima viva se puede alcanzar (se compara con la distancia Manhattan)."""
        for identificador in estado.vivas:
            victima = self.victimas[identificador]
            distancia = abs(estado.fila - victima.fila) + abs(estado.columna - victima.columna)
            ticks_restantes = victima.ticks_supervivencia - estado.tick
            if distancia <= ticks_restantes:
                return False
        return True

    def costo_paso(self, estado, sucesor):
        """Costo de un paso = víctimas que mueren en esa transición."""
        victimas_que_salieron = len(estado.vivas) - len(sucesor.vivas)
        victimas_rescatadas_ahora = len(sucesor.rescatadas) - len(estado.rescatadas)
        return victimas_que_salieron - victimas_rescatadas_ahora