import tkinter as tk

from interfaz.ventana import VentanaPrincipal


def main():
    ventana = tk.Tk()
    VentanaPrincipal(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
    