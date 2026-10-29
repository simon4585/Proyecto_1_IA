from modelo.mapa import Mapa
from modelo.victima import Victima
from problema.rescate import ProblemaRescate
from busqueda.bfs import bfs
from busqueda.ucs import ucs
from busqueda.iddfs import iddfs
from busqueda.astar import astar

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

    # 2) Ejecución de los algoritmos (BFS primero: es la referencia; A* al final)
    algoritmos = (bfs, ucs, iddfs, astar)
    resultados = [algoritmo(problema) for algoritmo in algoritmos]

    # 3) Tabla comparativa
    print("\n== Comparación de algoritmos ==")
    print(f"  {'Algoritmo':<10}{'Nodos':>8}{'Tiempo':>10}{'Rescatadas':>12}"
          f"{'Fallecidas':>12}{'Ticks':>7}")
    for r in resultados:
        fallecidas = len(VICTIMAS) - r.rescatadas
        print(f"  {r.algoritmo:<10}{r.nodos_expandidos:>8}{r.tiempo:>9.4f}s"
              f"{r.rescatadas:>12}{fallecidas:>12}{r.ticks:>7}")

    print("\n== Rutas encontradas ==")
    for r in resultados:
        print(f"  {r.algoritmo:<5}: {''.join(r.acciones)}")

    # 4) Ruta paso a paso de A*
    a = resultados[-1]
    print(f"\n== Ruta paso a paso ({a.algoritmo}) ==")
    for estado in a.camino:
        mostrar(estado)

    # 5) Comprobaciones de coherencia para cada algoritmo
    print("\n== Comprobaciones ==")
    referencia = resultados[0].rescatadas
    for r in resultados:
        estado = problema.estado_inicial()
        for accion in r.acciones:
            estado = problema.resultado(estado, accion)
        ok_ruta = estado == r.camino[-1]
        ok_meta = problema.es_objetivo(estado)
        ok_resc = r.rescatadas == referencia
        print(f"  {r.algoritmo:<5} ruta reproducible={ok_ruta}  "
                f"estado final es objetivo={ok_meta}  "
                f"mismas rescatadas que BFS={ok_resc}")


if __name__ == "__main__":
    main()