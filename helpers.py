from tkinter import *
import tkinter as tk
import re
from tkinter import messagebox as MessageBox

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")

class V_de_Opcion(tk.Toplevel, CenterWidgetMixin):
    def __init__(self, parent,title,text):
        super().__init__(parent)
        self.resultado = None
        self.title(title)
        self.text = text
        self.geometry("300x100")  # Define un tamaño fijo de 150x100 píxeles
        self.resizable(False, False)  # Evita que la ventana sea redimensionada
        self.build()
        self.center()
        

    def build(self):
        label = tk.Label(self, text=self.text)
        label.grid(row=0, columnspan=2, padx=30, pady=5,sticky='nsew')  # `sticky='nsew'` para expandir en las cuatro direcciones

        boton_si = tk.Button(self, text="Sí", command=self.elegir_si)
        boton_si.grid(row=1, column=0, padx=10, pady=5,sticky='ew')  # `sticky='ew'` para expandir horizontalmente

        boton_no = tk.Button(self, text="No", command=self.elegir_no)
        boton_no.grid(row=1, column=1, padx=10, pady=5,sticky='ew')

        # Configurar el peso de las columnas para que ocupen el espacio equitativamente
        self.grid_columnconfigure(0, weight=1)  # Primera columna
        self.grid_columnconfigure(1, weight=1)  # Segunda columna
        self.grid_rowconfigure(0, weight=1)     # Primera fila (para centrar el label)

    def elegir_si(self):
        self.resultado = "y" 
        self.destroy()

    def elegir_no(self):
        self.resultado = "n"
        self.destroy()

patron = r"^[a-jA-J](10|[1-9])$"