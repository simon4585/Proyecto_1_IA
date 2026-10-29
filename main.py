from modelo.mapa import Mapa
from modelo.victima import Victima
from problema.rescate import ProblemaRescate

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
    print(f"  tick={tick} pos=({fila},{col}) "
          f"vivas={sorted(vivas)} rescatadas={sorted(rescatadas)}")


def main():
    mapa = Mapa.desde_lineas(MAPA)
    problema = ProblemaRescate(mapa, VICTIMAS)

    # 1) Validación: ¿alguna víctima cae sobre una pared?
    print("== Validación de víctimas ==")
    for v in VICTIMAS:
        if not mapa.es_transitable(v.fila, v.columna):
            print(f"  AVISO: {v.id} está en ({v.fila},{v.columna}), que es pared")

    # 2) Estado inicial y sucesores
    estado = problema.estado_inicial()
    print("\n== Estado inicial ==")
    mostrar(estado)
    print("  t_max:", problema.t_max)
    print("  ¿es objetivo?:", problema.es_objetivo(estado))
    print("  acciones posibles:", [a for a, _ in problema.acciones(estado)])

    # 3) Simulación de una ruta manual
    ruta = ["E", "E", "E", "S", "S", "S", "E"]
    print("\n== Ruta manual:", ruta, "==")
    muertes = 0
    for accion in ruta:
        siguiente = problema.resultado(estado, accion)
        costo = problema.costo_paso(estado, siguiente)
        muertes += costo
        print(f"{accion}: costo del paso={costo}")
        mostrar(siguiente)
        estado = siguiente

    print("\n== Resumen ==")
    print("  rescatadas:", sorted(estado[3]))
    print("  muertes acumuladas:", muertes)
    print("  ¿es objetivo?:", problema.es_objetivo(estado))


if __name__ == "__main__":
    main()