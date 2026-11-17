from collections import namedtuple

# Un estado es una tupla con nombres. Al ser una tupla inmutable es hasheable,
# así que se puede guardar en conjuntos (visitados) y comparar con ==.
#   fila, columna : posición del agente
#   vivas         : frozenset con los ids de las víctimas que aún se pueden salvar
#   rescatadas    : frozenset con los ids de las víctimas ya rescatadas
#   tick          : movimientos realizados hasta ahora
Estado = namedtuple("Estado", ["fila", "columna", "vivas", "rescatadas", "tick"])