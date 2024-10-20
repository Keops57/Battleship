from tkinter import *
import tkinter as tk
import re
from tkinter import messagebox as MessageBox
import turtle

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

class TurtleWindow:
    def __init__(self, title, bg_color):
        # Crear una nueva ventana con Tkinter
        self.window = tk.Toplevel()
        self.window.title(title)
        
        # Crear un canvas para dibujar Turtle
        self.canvas = tk.Canvas(self.window, width=750, height=750)
        self.canvas.pack()
        
        # Asociar el canvas con un TurtleScreen
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor(bg_color)
        
        # Crear una tortuga asociada a esta pantalla
        self.turtle = turtle.RawTurtle(self.screen)
        self.turtle.pensize(3)
        self.turtle.speed(100)

        # Posicionar del cursor en la esquina sup izq
        self.x = -250
        self.y = -250

    def matriz(self,n):
        i = 0
        self.x = -250
        self.y = -250
        while i <= n:
            self.turtle.penup()
            self.turtle.setheading(90)
            self.turtle.goto(self.x,250)
            self.turtle.pendown()
            self.turtle.setheading(270)
            self.turtle.forward(500)
            i += 1
            self.x += 50
        i = 0
        while i <= n:
            self.turtle.penup()
            self.turtle.setheading(90)
            self.turtle.goto(-250,self.y)
            self.turtle.pendown()
            self.turtle.setheading(0)
            self.turtle.forward(500)
            i += 1
            self.y += 50

    def colocar (self):
        # Eje Y (filas): Letra -> -250 + (A=0, B=1, ..., J=9) * 50
        self.y = 250 - (ord("A") - ord('A')) * 50
            
        # Eje X (columnas): Número -> -250 + (columna - 1) * 50
        self.x = -250 + (1 - 1) * 50
        run = True
        patron = r"^[a-j](10|[1-9])$"
        while(run):

            orden = turtle.textinput("Donde quiere colocar los barcos", "Casillas de A-J 1-10")
            if orden:

                if re.match(patron, orden, re.IGNORECASE):
                    print(f"Coordenada ingresada: {orden}")
                    self.mover_a_casilla(orden)
                    run = False
                elif orden == "exit":
                        run = False
                
                else:
                    print("Valor invalido. ([a-j][1-10])")

    def mover_a_casilla(self, coordenada):
            """Traduce la coordenada (como 'A5') a coordenadas de Turtle y mueve la tortuga."""
            letra = coordenada[0].upper()  # Convertir la letra a mayúscula
            numero = int(coordenada[1:])   # Convertir el número a entero

            # Calcular las coordenadas en el lienzo de Turtle
            # Eje Y (filas): Letra -> -250 + (A=0, B=1, ..., J=9) * 50
            self.y = 250 - (ord(letra) - ord('A')) * 50
            
            # Eje X (columnas): Número -> -250 + (columna - 1) * 50
            self.x = -250 + (numero - 1) * 50

            # Mover la tortuga a la casilla correspondiente
            self.turtle.penup()
            self.turtle.goto(self.x, self.y)
    
    def dibujar_cuadrado(self,tam):
        self.x += 12
        self.y -= 12
        self.turtle.penup()  # Levanta el lápiz para mover sin dibujar
        self.turtle.goto(self.x, self.y)  # Mueve la tortuga a la posición especificada
        self.turtle.pendown()  # Baja el lápiz para empezar a dibujar
        self.turtle.begin_fill()  # Comienza el relleno
        for _ in range(4):  # Dibuja un cuadrado
            self.turtle.forward(tam)
            self.turtle.right(90)
        self.turtle.end_fill()  # Termina el relleno

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