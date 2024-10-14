import turtle
from tkinter import *
import tkinter as tk
import re
import database as db
from tkinter import messagebox as MessageBox

window = turtle.Screen()
window.title("Battleship")
window.bgcolor("#144c74")
window.setup(750, 750)

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

class Tortuga(turtle.Turtle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pensize(3)
        self.speed(100)
        self.shape("circle")
        self.color("black")
        self.x = -250
        self.y = -250

    def matriz(self,n):
        i = 0
        self.x = -250
        self.y = -250
        while i <= n:
            self.penup()
            self.setheading(90)
            self.goto(self.x,250)
            self.pendown()
            self.setheading(270)
            self.forward(500)
            i += 1
            self.x += 50
        i = 0
        while i <= n:
            self.penup()
            self.setheading(90)
            self.goto(-250,self.y)
            self.pendown()
            self.setheading(0)
            self.forward(500)
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
            self.penup()
            self.goto(self.x, self.y)
            #self.stamp()  # Opcional: Dejar una marca
            
    def dibujar_cuadrado(self,tam):
        self.x += 12
        self.y -= 12
        turtle.penup()  # Levanta el lápiz para mover sin dibujar
        turtle.goto(self.x, self.y)  # Mueve la tortuga a la posición especificada
        turtle.pendown()  # Baja el lápiz para empezar a dibujar
        turtle.begin_fill()  # Comienza el relleno
        for _ in range(4):  # Dibuja un cuadrado
            turtle.forward(tam)
            turtle.right(90)
        turtle.end_fill()  # Termina el relleno

class Ventana(tk.Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.resultado = None
        self.geometry("150x100")  # Define un tamaño fijo de 150x100 píxeles
        self.resizable(False, False)  # Evita que la ventana sea redimensionada
        self.build()
        self.center()

    def build(self):
        self.title("Disparo")
        label = tk.Label(self, text="¿Desea disparar?")
        label.grid(row=0, columnspan=2, padx=30, pady=5)

        boton_si = tk.Button(self, text="Sí", command=self.elegir_si)
        boton_si.grid(row=1, column=0, padx=10, pady=5)

        boton_no = tk.Button(self, text="No", command=self.elegir_no)
        boton_no.grid(row=1, column=1, padx=10, pady=5)

    def elegir_si(self):
        self.resultado = "y" 
        self.destroy()

    def elegir_no(self):
        self.resultado = "n"
        self.destroy()

class Juego:
    def __init__(self):
        self.grid = Tortuga()
        self.grid.matriz(10)
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal

    def jugar(self):
        tablero = db.tablero
        while True:
            ventana = Ventana(self.root)
            ventana.wait_window()  # Espera a que el usuario elija una opción

            eleccion = ventana.resultado
            if eleccion == "y":
                coordenada = turtle.textinput("Colocar", "Ingrese una coordenada (A-J 1-10):")
                if coordenada.lower() and re.match(r"^[a-jA-J](10|[1-9])$", coordenada):
                    bomba = tablero.disparar(coordenada)
                    if bomba == True:
                        turtle.color("Red")
                        self.grid.mover_a_casilla(coordenada)
                        self.grid.dibujar_cuadrado(25)
                    elif bomba == False:
                        turtle.color("White")
                        self.grid.mover_a_casilla(coordenada)
                        self.grid.dibujar_cuadrado(25)
                    elif bomba == None:
                        MessageBox.showwarning("Error", "Ya se disparo en esa casilla, pruebe otra")
                    

                else:
                    print("Coordenada inválida.")
            elif eleccion == "n":
                break

        self.root.destroy()  # Cierra la ventana principal de Tkinter
        window.bye()  # Cierra la ventana de Turtle

# Ejecutar el juego
juego = Juego()