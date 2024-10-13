import turtle
import sys
import re

window = turtle.Screen()
window.title("Battleship")
window.bgcolor("#144c74")
window.setup(750, 750)



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
                    #run = False
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
            self.stamp()  # Opcional: Dejar una marca

    def dibujar_cuadrado(self,tam):
        self.x += 12
        self.y -= 12
        turtle.penup()  # Levanta el lápiz para mover sin dibujar
        turtle.goto(self.x, self.y)  # Mueve la tortuga a la posición especificada
        turtle.pendown()  # Baja el lápiz para empezar a dibujar
        turtle.color("white")
        turtle.begin_fill()  # Comienza el relleno
        for _ in range(4):  # Dibuja un cuadrado
            turtle.forward(tam)
            turtle.right(90)
        turtle.end_fill()  # Termina el relleno

grid = Tortuga()
grid.matriz(10)
grid.colocar()
grid.dibujar_cuadrado(25)
