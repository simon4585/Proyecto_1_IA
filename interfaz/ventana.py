import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from io_archivos.lector import cargar_mapa, cargar_victimas, ErrorDeArchivo
from problema.rescate import ProblemaRescate
from busqueda.bfs import bfs
from busqueda.ucs import ucs
from busqueda.iddfs import iddfs
from busqueda.astar import astar

# Algoritmos disponibles en el menú desplegable
ALGORITMOS = {"BFS": bfs, "UCS": ucs, "IDDFS": iddfs, "A*": astar}

FUENTE = "Segoe UI"

TAMANO_CELDA = 60

# Colores de la interfaz
COLOR_FONDO = "#FFFFFF"
COLOR_TARJETA = "#FFFFFF"
COLOR_TITULO_TARJETA = "#FFFFFF"
COLOR_BORDE = "#D9DDE3"
COLOR_TEXTO = "#1F2937"
COLOR_TEXTO_CLARO = "#FFFFFF"
COLOR_ENCABEZADO = "#3780FF"
COLOR_BOTON_PRINCIPAL = "#3780FF"
COLOR_BOTON_PRINCIPAL_PRESIONADO = "#0A2B63"
COLOR_BOTON_SECUNDARIO = "#FFFFFF"
COLOR_BOTON_SECUNDARIO_PRESIONADO = "#F3F4F6"
COLOR_LECTURA_OK = "#1E7B34"
COLOR_LECTURA_ERROR = "#C62828"

# Colores del mapa
COLOR_PARED = "#000000"
COLOR_LIBRE = "#FFFFFF"
COLOR_LINEA_CELDA = "#E5E7EB"
COLOR_AGENTE = "#2F6FED"
COLOR_VICTIMA_VIVA = "#EEA827"
COLOR_VICTIMA_RESCATADA = "#68BB2D"
COLOR_VICTIMA_MUERTA = "#E0271A"


class VentanaPrincipal:
    """Ventana de la aplicación: archivos, configuración, mapa animado y resultados."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Agente de Rescate")
        self.ventana.configure(bg=COLOR_FONDO)
        self.maximizar_ventana()

        # Datos cargados desde los archivos
        self.mapa = None
        self.victimas = None
        self.ruta_mapa = ""
        self.ruta_victimas = ""

        # Datos de la simulación
        self.resultados = {}          # nombre del algoritmo -> ResultadoBusqueda
        self.camino_animado = []      # lista de estados que se van dibujando
        self.indice_tick = 0          # posición actual dentro de camino_animado
        self.identificador_animacion = None

        self.construir_pantalla_principal()
        self.pantalla_principal.pack(fill="both", expand=True)

    def maximizar_ventana(self):
        """Abre la ventana ocupando toda la pantalla (con sus botones de ventana)."""
        try:
            self.ventana.state("zoomed")
        except tk.TclError:
            try:
                self.ventana.attributes("-zoomed", True)
            except tk.TclError:
                pass

    # Botones y tarjetas
    def crear_boton_principal(self, padre, texto, comando, tamano_letra):
        return tk.Button(padre, text=texto, command=comando,
                         bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_CLARO,
                         activebackground=COLOR_BOTON_PRINCIPAL_PRESIONADO,
                         activeforeground=COLOR_TEXTO_CLARO,
                         font=(FUENTE, tamano_letra, "bold"), relief="flat",
                         cursor="hand2")

    def crear_boton_secundario(self, padre, texto, comando):
        return tk.Button(padre, text=texto, command=comando,
                         bg=COLOR_BOTON_SECUNDARIO, fg=COLOR_TEXTO,
                         activebackground=COLOR_BOTON_SECUNDARIO_PRESIONADO,
                         activeforeground=COLOR_TEXTO,
                         font=(FUENTE, 11), relief="flat", pady=8,
                         highlightthickness=1, highlightbackground=COLOR_BORDE,
                         cursor="hand2")

    def crear_tarjeta(self, padre, titulo, expandir=False):
        tarjeta = tk.Frame(padre, bg=COLOR_TARJETA,
                           highlightthickness=1, highlightbackground=COLOR_BORDE)
        if expandir:
            tarjeta.pack(fill="both", expand=True, pady=6)
        else:
            tarjeta.pack(fill="x", pady=6)

        etiqueta_titulo = tk.Label(tarjeta, text=titulo, bg=COLOR_TITULO_TARJETA,
                                   fg=COLOR_TEXTO, font=(FUENTE, 12, "bold"),
                                   anchor="w", padx=12, pady=8)
        etiqueta_titulo.pack(fill="x")

        cuerpo = tk.Frame(tarjeta, bg=COLOR_TARJETA)
        cuerpo.pack(fill="both", expand=expandir, padx=10, pady=10)
        return etiqueta_titulo, cuerpo

    # Pantalla principal
    def construir_pantalla_principal(self):
        self.pantalla_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)

        encabezado = tk.Label(self.pantalla_principal,
                              text="Agente de Rescate con Víctimas en Riesgo",
                              bg=COLOR_ENCABEZADO, fg=COLOR_TEXTO_CLARO,
                              font=(FUENTE, 20, "bold"), pady=14)
        encabezado.pack(fill="x")

        # Zona desplazable: si la pantalla es pequeña, se baja con la barra o con
        # la rueda del mouse. Así los resultados se pueden ver en cualquier computador.
        contenedor = tk.Frame(self.pantalla_principal, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True)

        barra_vertical = tk.Scrollbar(contenedor, orient="vertical")
        barra_vertical.pack(side="right", fill="y")

        self.lienzo_pantalla = tk.Canvas(contenedor, bg=COLOR_FONDO,
                                         highlightthickness=0, yscrollincrement=30,
                                         yscrollcommand=barra_vertical.set)
        self.lienzo_pantalla.pack(side="left", fill="both", expand=True)
        barra_vertical.config(command=self.lienzo_pantalla.yview)

        # Todo el contenido va dentro de este Frame, que se coloca dentro del Canvas
        zona_central = tk.Frame(self.lienzo_pantalla, bg=COLOR_FONDO)
        self.ventana_interna = self.lienzo_pantalla.create_window(
            (0, 0), window=zona_central, anchor="nw")
        self.lienzo_pantalla.bind("<Configure>", self.ajustar_ancho_zona_central)
        zona_central.bind("<Configure>", self.actualizar_region_desplazable)
        self.ventana.bind_all("<MouseWheel>", self.desplazar_con_rueda)

        columna_izquierda = tk.Frame(zona_central, bg=COLOR_FONDO)
        columna_izquierda.pack(side="left", fill="y", padx=(15, 0), pady=10)
        columna_derecha = tk.Frame(zona_central, bg=COLOR_FONDO)
        columna_derecha.pack(side="left", fill="both", expand=True,
                             padx=(15, 15), pady=10)

        self.construir_tarjeta_archivos(columna_izquierda)
        self.construir_tarjeta_configuracion(columna_izquierda)
        self.construir_tarjeta_resultados(columna_izquierda)
        self.construir_tarjeta_mapa(columna_derecha)
        self.construir_leyenda(columna_derecha)

    def ajustar_ancho_zona_central(self, evento):
        """Hace que el contenido ocupe todo el ancho de la ventana."""
        self.lienzo_pantalla.itemconfigure(self.ventana_interna, width=evento.width)

    def actualizar_region_desplazable(self, evento):
        """Le dice al Canvas hasta dónde se puede desplazar (el tamaño del contenido)."""
        self.lienzo_pantalla.configure(scrollregion=self.lienzo_pantalla.bbox("all"))

    def desplazar_con_rueda(self, evento):
        """Mueve la pantalla con la rueda del mouse.

        Si el mouse está sobre el cuadro de resultados, la rueda desplaza ese cuadro.
        """
        if evento.widget is self.cuadro_estadisticas:
            return
        if evento.delta > 0:
            self.lienzo_pantalla.yview_scroll(-1, "units")
        else:
            self.lienzo_pantalla.yview_scroll(1, "units")

    def construir_tarjeta_archivos(self, columna):
        """Botones 'Examinar' y estado de lectura de cada archivo."""
        titulo, cuerpo = self.crear_tarjeta(columna, "Archivos de entrada")

        boton_mapa = self.crear_boton_secundario(cuerpo, "Examinar mapa.txt",
                                                 self.seleccionar_mapa)
        boton_mapa.pack(fill="x")
        self.etiqueta_mapa = tk.Label(cuerpo, text="Ningún archivo seleccionado",
                                      bg=COLOR_TARJETA, fg=COLOR_TEXTO,
                                      font=(FUENTE, 9), wraplength=430,
                                      justify="left", anchor="w")
        self.etiqueta_mapa.pack(fill="x", pady=(3, 10))

        boton_victimas = self.crear_boton_secundario(cuerpo, "Examinar victimas.txt",
                                                     self.seleccionar_victimas)
        boton_victimas.pack(fill="x")
        self.etiqueta_victimas = tk.Label(cuerpo, text="Ningún archivo seleccionado",
                                          bg=COLOR_TARJETA, fg=COLOR_TEXTO,
                                          font=(FUENTE, 9), wraplength=430,
                                          justify="left", anchor="w")
        self.etiqueta_victimas.pack(fill="x", pady=(3, 0))

    def construir_tarjeta_configuracion(self, columna):
        """Algoritmo, pausa entre ticks y botón 'Iniciar Rescate'."""
        titulo, cuerpo = self.crear_tarjeta(columna, "Configuración")

        tk.Label(cuerpo, text="Algoritmo:", bg=COLOR_TARJETA, fg=COLOR_TEXTO,
                 font=(FUENTE, 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.menu_algoritmo = ttk.Combobox(cuerpo, values=list(ALGORITMOS.keys()),
                                           state="readonly", width=10,
                                           font=(FUENTE, 11))
        self.menu_algoritmo.current(0)
        self.menu_algoritmo.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        tk.Label(cuerpo, text="Pausa entre ticks (ms):", bg=COLOR_TARJETA,
                 fg=COLOR_TEXTO, font=(FUENTE, 11)).grid(row=1, column=0, padx=5,
                                                         pady=5, sticky="w")
        self.caja_pausa = tk.Spinbox(cuerpo, from_=50, to=1500, increment=50,
                                     width=8, font=(FUENTE, 11), justify="center")
        self.caja_pausa.delete(0, tk.END)
        self.caja_pausa.insert(0, "500")
        self.caja_pausa.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        cuerpo.columnconfigure(0, weight=1)

        boton_iniciar = self.crear_boton_principal(columna, "Iniciar Rescate",
                                                   self.iniciar_rescate, 14)
        boton_iniciar.config(pady=10)
        boton_iniciar.pack(fill="x", pady=6)

    def construir_tarjeta_resultados(self, columna):
        """Cuadro de texto para las estadísticas finales (14 líneas, se ven completas)."""
        titulo, cuerpo = self.crear_tarjeta(columna, "Resultados", expandir=True)

        barra = tk.Scrollbar(cuerpo)
        barra.pack(side="right", fill="y")
        self.cuadro_estadisticas = tk.Text(cuerpo, height=14, width=64,
                                           font=("Courier", 9), relief="flat",
                                           bg=COLOR_TEXTO_CLARO, fg=COLOR_TEXTO,
                                           highlightthickness=1,
                                           highlightbackground=COLOR_BORDE,
                                           yscrollcommand=barra.set)
        self.cuadro_estadisticas.pack(side="left", fill="both", expand=True)
        barra.config(command=self.cuadro_estadisticas.yview)

    def construir_tarjeta_mapa(self, columna):
        """Tarjeta con el mapa dibujado; su título muestra el tick actual."""
        self.etiqueta_tick, cuerpo = self.crear_tarjeta(columna, "Mapa - Tick: 0")
        self.lienzo = tk.Canvas(cuerpo, width=400, height=300, bg=COLOR_TARJETA,
                                highlightthickness=0)
        self.lienzo.pack(pady=5)

    def construir_leyenda(self, columna):
        """Leyenda de colores debajo del mapa."""
        leyenda = tk.Frame(columna, bg=COLOR_TARJETA,
                           highlightthickness=1, highlightbackground=COLOR_BORDE)
        leyenda.pack(fill="x", pady=6)

        elementos = [(COLOR_AGENTE, "Agente"),
                     (COLOR_VICTIMA_VIVA, "Víctimas vivas"),
                     (COLOR_VICTIMA_RESCATADA, "Víctimas rescatadas"),
                     (COLOR_VICTIMA_MUERTA, "Víctimas fallecidas"),
                     (COLOR_PARED, "Obstáculos")]
        for color, nombre in elementos:
            tk.Label(leyenda, bg=color, width=2).pack(side="left", padx=(15, 5), pady=15)
            tk.Label(leyenda, text=nombre, bg=COLOR_TARJETA, fg=COLOR_TEXTO,
                     font=(FUENTE, 10)).pack(side="left")

    # Carga de archivos
    def seleccionar_mapa(self):
        ruta = filedialog.askopenfilename(title="Seleccione mapa.txt",
                                          filetypes=[("Texto", "*.txt")])
        if ruta == "":
            return
        self.ruta_mapa = ruta
        self.detener_animacion()
        try:
            self.mapa = cargar_mapa(ruta)
            self.etiqueta_mapa.config(text="OK  " + ruta, fg=COLOR_LECTURA_OK)
        except ErrorDeArchivo as error:
            self.mapa = None
            self.etiqueta_mapa.config(text="ERROR: " + str(error), fg=COLOR_LECTURA_ERROR)
            return

        self.dibujar_mapa_vacio()

        if self.ruta_victimas != "":
            self.leer_victimas()

    def seleccionar_victimas(self):
        if self.mapa is None:
            messagebox.showwarning("Falta el mapa", "Primero cargue un mapa válido.")
            return
        ruta = filedialog.askopenfilename(title="Seleccione victimas.txt",
                                          filetypes=[("Texto", "*.txt")])
        if ruta == "":
            return
        self.ruta_victimas = ruta
        self.detener_animacion()
        self.leer_victimas()

    def leer_victimas(self):
        """Lee el archivo de víctimas, actualiza el indicador y dibuja la vista previa."""
        try:
            self.victimas, advertencias = cargar_victimas(self.ruta_victimas, self.mapa)
            texto = "OK  " + self.ruta_victimas
            if len(advertencias) > 0:
                texto = texto + "  (" + advertencias[0] + ")"
            self.etiqueta_victimas.config(text=texto, fg=COLOR_LECTURA_OK)
        except ErrorDeArchivo as error:
            self.victimas = None
            self.etiqueta_victimas.config(text="ERROR: " + str(error),
                                          fg=COLOR_LECTURA_ERROR)
            return

        problema = ProblemaRescate(self.mapa, self.victimas)
        self.dibujar_estado(problema.estado_inicial())

    # Ejecución de los algoritmos
    def leer_pausa(self):
        """Lee la pausa entre ticks. Si el valor no es un número, usa 500 ms."""
        try:
            pausa = int(self.caja_pausa.get())
        except ValueError:
            pausa = 500
        if pausa < 50:
            pausa = 50
        return pausa

    def iniciar_rescate(self):
        if self.mapa is None or self.victimas is None:
            messagebox.showwarning("Faltan datos", "Cargue el mapa y las víctimas.")
            return

        self.detener_animacion()
        self.cuadro_estadisticas.delete("1.0", tk.END)

        # Se vuelve arriba para ver el mapa mientras se anima
        self.lienzo_pantalla.yview_moveto(0.0)

        problema = ProblemaRescate(self.mapa, self.victimas)
        self.resultados = {}
        for nombre, algoritmo in ALGORITMOS.items():
            self.resultados[nombre] = algoritmo(problema)

        resultado_elegido = self.resultados[self.menu_algoritmo.get()]
        if len(resultado_elegido.camino) == 0:
            messagebox.showinfo("Sin solución", "El algoritmo no encontró ningún camino.")
            return

        self.camino_animado = resultado_elegido.camino
        self.indice_tick = 0
        self.avanzar_tick()

    def avanzar_tick(self):
        """Dibuja el estado actual y programa el siguiente tick."""
        estado = self.camino_animado[self.indice_tick]
        es_ultimo_estado = (self.indice_tick == len(self.camino_animado) - 1)
        self.dibujar_estado(estado, es_ultimo_estado)

        if es_ultimo_estado:
            self.mostrar_estadisticas()
            return

        self.indice_tick = self.indice_tick + 1
        self.identificador_animacion = self.ventana.after(self.leer_pausa(),
                                                          self.avanzar_tick)

    def detener_animacion(self):
        """Cancela una animacion que esté en curso."""
        if self.identificador_animacion is not None:
            self.ventana.after_cancel(self.identificador_animacion)
            self.identificador_animacion = None

    # Dibujo
    def dibujar_mapa_vacio(self):
        """Dibuja solo las paredes y las celdas libres"""
        self.lienzo.config(width=self.mapa.columnas * TAMANO_CELDA,
                           height=self.mapa.filas * TAMANO_CELDA)
        self.lienzo.delete("all")
        for fila in range(self.mapa.filas):
            for columna in range(self.mapa.columnas):
                x_izquierda = columna * TAMANO_CELDA
                y_arriba = fila * TAMANO_CELDA
                if self.mapa.cuadricula[fila][columna] == "#":
                    color = COLOR_PARED
                else:
                    color = COLOR_LIBRE
                self.lienzo.create_rectangle(x_izquierda, y_arriba,
                                             x_izquierda + TAMANO_CELDA,
                                             y_arriba + TAMANO_CELDA,
                                             fill=color, outline=COLOR_LINEA_CELDA)

    def dibujar_estado(self, estado, es_ultimo_estado=False):
        """Dibuja el mapa, las víctimas y el agente según un estado"""
        fila_agente, columna_agente, vivas, rescatadas, tick = estado
        self.dibujar_mapa_vacio()
        self.etiqueta_tick.config(text="Mapa - Tick: " + str(tick))

        for victima in self.victimas:
            x_izquierda = victima.columna * TAMANO_CELDA
            y_arriba = victima.fila * TAMANO_CELDA
            if victima.identificador in rescatadas:
                color = COLOR_VICTIMA_RESCATADA
                texto = victima.identificador
            elif victima.identificador in vivas and not es_ultimo_estado:
                color = COLOR_VICTIMA_VIVA
                ticks_restantes = victima.ticks_supervivencia - tick
                texto = victima.identificador + "\n" + str(ticks_restantes)
            else:
                color = COLOR_VICTIMA_MUERTA
                texto = victima.identificador
            self.lienzo.create_rectangle(x_izquierda + 4, y_arriba + 4,
                                         x_izquierda + TAMANO_CELDA - 4,
                                         y_arriba + TAMANO_CELDA - 4,
                                         fill=color, outline="")
            self.lienzo.create_text(x_izquierda + TAMANO_CELDA // 2,
                                    y_arriba + TAMANO_CELDA // 2,
                                    text=texto, font=(FUENTE, 11, "bold"),
                                    fill=COLOR_TEXTO)

        x_agente = columna_agente * TAMANO_CELDA
        y_agente = fila_agente * TAMANO_CELDA
        self.lienzo.create_oval(x_agente + 2, y_agente + 2,
                                x_agente + 20, y_agente + 20,
                                fill=COLOR_AGENTE, outline=COLOR_TEXTO_CLARO, width=2)

    # Estadísticas
    def mostrar_estadisticas(self):
        """Escribe el resultado de la simulación y la tabla comparativa."""
        resultado = self.resultados[self.menu_algoritmo.get()]
        total = len(self.victimas)
        rescatadas = resultado.rescatadas
        fallecidas = total - rescatadas

        linea = "+" + "-" * 62 + "+\n"
        texto = linea
        texto += "| RESULTADO DE LA SIMULACION (" + resultado.algoritmo + ")\n"
        texto += "| Victimas totales   : " + str(total) + "\n"
        texto += "| Victimas rescatadas: " + str(rescatadas) + "\n"
        texto += "| Victimas fallecidas: " + str(fallecidas) + "\n"
        texto += "| Ticks totales      : " + str(resultado.ticks) + "\n"
        texto += linea
        texto += "| COMPARACION DE ALGORITMOS\n"
        texto += "| Algoritmo | Nodos | Tiempo    | Rescatadas | Fallecidas\n"
        for nombre, otro in self.resultados.items():
            tiempo_texto = format(otro.tiempo, ".4f") + "s"
            texto += ("| " + nombre.ljust(9)
                      + " | " + str(otro.nodos_expandidos).ljust(5)
                      + " | " + tiempo_texto.ljust(9)
                      + " | " + str(otro.rescatadas).ljust(10)
                      + " | " + str(total - otro.rescatadas) + "\n")
        texto += linea

        self.cuadro_estadisticas.delete("1.0", tk.END)
        self.cuadro_estadisticas.insert(tk.END, texto)

        # Si la pantalla es pequeña, se baja hasta los resultados para que se vean
        self.lienzo_pantalla.yview_moveto(1.0)