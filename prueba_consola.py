from io_archivos.lector import cargar_mapa, cargar_victimas
from problema.rescate import ProblemaRescate
from busqueda.bfs import bfs
from busqueda.ucs import ucs
from busqueda.iddfs import iddfs
from busqueda.astar import astar

mapa = cargar_mapa("data/mapa.txt")
victimas, advertencias = cargar_victimas("data/victimas.txt", mapa)
problema = ProblemaRescate(mapa, victimas)

for algoritmo in (bfs, ucs, iddfs, astar):
    resultado = algoritmo(problema)
    print(resultado.algoritmo, "| nodos:", resultado.nodos_expandidos,
          "| tiempo:", round(resultado.tiempo, 4),
          "| rescatadas:", resultado.rescatadas,
          "| ticks:", resultado.ticks,
          "| camino:", "".join(resultado.acciones))