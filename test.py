import turtle
import tkinter as tk
import re

class TurtleWindow:
    def __init__(self, title, bg_color):
        # Crear una nueva ventana con Tkinter
        self.window = tk.Toplevel()
        self.window.title(title)
        
        # Crear un canvas para dibujar Turtle
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack()
        
        # Asociar el canvas con un TurtleScreen
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor(bg_color)
        
        # Crear una tortuga asociada a esta pantalla
        self.turtle = turtle.RawTurtle(self.screen)
        self.turtle.speed(1)

    def draw_circle(self, radius=50):
        self.turtle.circle(radius)

    def draw_square(self, side=100):
        for _ in range(4):
            self.turtle.forward(side)
            self.turtle.right(90)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controlador de Ventanas")

        # Crear dos ventanas de Turtle
        self.window1 = TurtleWindow("Ventana 1", "lightblue")
        self.window2 = TurtleWindow("Ventana 2", "lightgreen")

        # Crear botones para controlar las tortugas en cada ventana
        btn1 = tk.Button(root, text="Dibujar Círculo en Ventana 1", 
                        command=self.draw_circle_in_window1)
        btn1.pack()

        btn2 = tk.Button(root, text="Dibujar Cuadrado en Ventana 2", 
                        command=self.draw_square_in_window2)
        btn2.pack()

    def draw_circle_in_window1(self):
        self.window1.draw_circle()

    def draw_square_in_window2(self):
        self.window2.draw_square()

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


# Crear la ventana principal de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
