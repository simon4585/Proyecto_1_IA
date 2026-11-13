from io_archivos.lector import cargar_mapa, cargar_victimas, ErrorDeArchivo
from problema.rescate import ProblemaRescate
from busqueda.bfs import bfs
from busqueda.ucs import ucs
from busqueda.iddfs import iddfs
from busqueda.astar import astar


def main():
    try:
        mapa = cargar_mapa("data/mapa.txt")
        victimas, advertencias = cargar_victimas("data/victimas.txt", mapa)
    except ErrorDeArchivo as error:
        print("ERROR de lectura:", error)
        return

    print(f"Mapa {mapa.filas}x{mapa.columnas}, {len(victimas)} víctimas")
    for aviso in advertencias:
        print("  AVISO:", aviso)

    problema = ProblemaRescate(mapa, victimas)
    resultados = [algoritmo(problema) for algoritmo in (bfs, ucs, iddfs, astar)]

    print(f"\n  {'Algoritmo':<10}{'Nodos':>8}{'Tiempo':>10}{'Rescatadas':>12}"
          f"{'Fallecidas':>12}{'Ticks':>7}")
    for r in resultados:
        print(f"  {r.algoritmo:<10}{r.nodos_expandidos:>8}{r.tiempo:>9.4f}s"
              f"{r.rescatadas:>12}{len(victimas) - r.rescatadas:>12}{r.ticks:>7}")


if __name__ == "__main__":
    main()