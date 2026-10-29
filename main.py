from modelo.mapa import Mapa
from modelo.victima import Victima
from problema.rescate import ProblemaRescate
from busqueda.bfs import bfs

MAPA = """##########
#S...#...#
#.##.#.#.#
#....#.#.#
#.##...#.#
#....#...#
##########""".splitlines()

VICTIMAS = [
    Victima("V1", 1, 4, 5),
    Victima("V2", 3, 7, 12),
    Victima("V3", 5, 2, 3),
    Victima("V4", 2, 8, 20),
    Victima("V5", 4, 5, 7),
]


def mostrar(estado):
    fila, col, vivas, rescatadas, tick = estado
    print(f"  tick={tick:2d} pos=({fila},{col}) "
          f"vivas={sorted(vivas)} rescatadas={sorted(rescatadas)}")


def main():
    mapa = Mapa.desde_lineas(MAPA)
    problema = ProblemaRescate(mapa, VICTIMAS)

    # 1) Validación de datos de entrada
    print("== Validación de víctimas ==")
    for v in VICTIMAS:
        if not mapa.es_transitable(v.fila, v.columna):
            print(f"  AVISO: {v.id} está en ({v.fila},{v.columna}), que es pared")

    # 2) Ejecución de BFS
    print("\n== Resultado de BFS ==")
    r = bfs(problema)
    print("  Rescatadas      :", r.rescatadas, "de", len(VICTIMAS))
    print("  Fallecidas      :", len(VICTIMAS) - r.rescatadas)
    print("  Ticks totales   :", r.ticks)
    print("  Nodos expandidos:", r.nodos_expandidos)
    print(f"  Tiempo          : {r.tiempo:.4f} s")
    print("  Acciones        :", "".join(r.acciones))

    # 3) Reproducción de la ruta tick a tick
    print("\n== Ruta paso a paso ==")
    for estado in r.camino:
        mostrar(estado)

    # 4) Comprobaciones de coherencia
    print("\n== Comprobaciones ==")
    estado = problema.estado_inicial()
    for accion in r.acciones:
        estado = problema.resultado(estado, accion)
    print("  Repetir las acciones llega al estado final:", estado == r.camino[-1])
    print("  El estado final es objetivo               :", problema.es_objetivo(estado))
    print("  Largo del camino = acciones + 1           :",
          len(r.camino) == len(r.acciones) + 1)


if __name__ == "__main__":
    main()