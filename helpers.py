import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import turtle
import re
import client as cl

patron = r"^[a-jA-J]([0-9])$"

# noinspection PyUnresolvedReferences
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
        self.turtle.speed(300) # 300

        # Posicionar del cursor en la esquina sup izq
        self.x = -250
        self.y = -250

    def matriz(self,n):
        letras = ['A','B','C','D','E','F','G','H','I','J']
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
            self.x += 25
            if i != 10:
                self.canvas.create_text(self.x, -280, text=f"{i}", font=("Comic Sans ms", 24), fill="black")
            i += 1
            self.x += 25
        i = 0
        while i <= n:
            self.turtle.penup()
            self.turtle.setheading(90)
            self.turtle.goto(-250,self.y)
            self.turtle.pendown()
            self.turtle.setheading(0)
            self.turtle.forward(500)
            self.y += 25
            if i != 10:
                self.canvas.create_text(-280, self.y, text=f"{letras[i]}", font=("Comic Sans ms", 24), fill="black")
            i += 1
            self.y += 25

    def colocar (self):
        # Eje Y (filas): Letra -> -250 + (A=0, B=1, ..., J=9) * 50
        self.y = 250 - (ord("A") - ord('A')) * 50
            
        # Eje X (columnas): Número -> -250 + (columna - 1) * 50
        self.x = -250 + (1 - 1) * 50
        run = True
        while run:

            orden = turtle.textinput("Donde quiere colocar los barcos", "Casillas de A-J 0-9")
            if orden:

                if re.match(patron, orden, re.IGNORECASE):
                    print(f"Coordenada ingresada: {orden}")
                    self.mover_a_casilla(orden)
                    run = False
                elif orden == "exit":
                        run = False
                
                else:
                    print("Valor invalido. ([a-j][0-9])")

    def mover_a_casilla(self, coordenada):
            """Traduce la coordenada (como 'A5') a coordenadas de Turtle y mueve la tortuga."""
            letra = coordenada[0].upper()  # Convertir la letra a mayúscula
            numero = int(coordenada[1:])   # Convertir el número a entero

            # Calcular las coordenadas en el lienzo de Turtle

            # Eje X (columnas): Número -> -250 + (columna - 1) * 50
            self.x = -200 + (numero - 1) * 50
            
            # Eje Y (filas): Letra -> -250 + (A=0, B=1, ..., J=9) * 50
            self.y = 250 - (ord(letra) - ord('A')) * 50
            
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

class V_de_Casillas(tk.Toplevel, CenterWidgetMixin):
    def __init__(self, parent, title, text,lim):
        super().__init__(parent)
        self.resultado = None
        self.lim = lim
        self.cI = ""
        self.cF = ""
        self.title(title)
        self.text = text
        self.geometry("500x100")
        self.casillas_a_marcar = []
        self.resizable(False, False)  # Evita que la ventana sea redimensionada
        self.build()
        self.center()

    def build(self):
        """Construye los widgets de la ventana."""
        label = tk.Label(self, text=self.text)
        label.grid(row=0, columnspan=2, padx=30, pady=5, sticky='nsew')

        self.cinicio = tk.Entry(self)
        self.cinicio.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

        self.cfinal = tk.Entry(self)
        self.cfinal.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        boton_confirmar = tk.Button(self, text="Confirmar", command=self.confirmar)
        boton_confirmar.grid(row=2, columnspan=2, padx=10, pady=5, sticky='ew')

        # Configuración de peso para expandir columnas
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def confirmar(self):
        """Valida las entradas y cierra la ventana."""
        self.cI = self.cinicio.get().strip()
        self.cF = self.cfinal.get().strip()

        lista_numeros = [str(x) for x in range(0, 10)]
        lista_letras = ["a","b","c","d","e","f","g","h","i","j"]

        if not self.cI or not self.cF:
            messagebox.showerror("Error", "Ambas coordenadas son obligatorias.")
            return  # No cerrar la ventana si los campos están vacíos
        
        
        if self.cI[0] == self.cF[0] and self.cI[1] in lista_numeros and self.cF[1] in lista_numeros:
            valid = int(self.cF[1]) - int(self.cI[1]) 
            print(valid)

            if valid <=0:
                messagebox.showerror("Error", "Posicionamiento invalido (Coloque las casillas de izq a der o de arriba a abajo)")
                return  # No cerrar la ventana si los campos están vacíos
            
            elif valid == self.lim:
                for i in range(int(self.cI[1]), int(self.cF[1]) + 1):
                    self.casillas_a_marcar.append(f"{self.cI[0]}{i}")
                print("Coordenadas Validas")
                print(f"Coordenadas Actuales: {self.casillas_a_marcar}")
            
            else:
                messagebox.showerror("Error", "Posicionamiento invalido")
                return  # No cerrar la ventana si los campos están vacíos


        elif self.cI[1] == self.cF[1] and self.cI[0] in lista_letras and self.cF[0] in lista_letras:

            valid = ord(self.cF[0]) - ord(self.cI[0]) 
            print(valid)

            if valid <=0:
                messagebox.showerror("Error", "Posicionamiento invalido (Coloque las casillas de izq a der o de arriba a abajo)")
                return  # No cerrar la ventana si los campos están vacíos
            
            elif valid == self.lim:
                for i in range(ord(self.cI[0]) , ord(self.cF[0]) + 1):
                    self.casillas_a_marcar.append(f"{chr(i)}{self.cF[1]}")
                print("Coordenadas Validas")
                print(f"Coordenadas Actuales: {self.casillas_a_marcar}")

            else:
                messagebox.showerror("Error", "Posicionamiento invalido")
                return  # No cerrar la ventana si los campos están vacíos
            
        else:
            messagebox.showerror("Error", "Posicionamiento invalido")
            return
        

        self.resultado = "y"  # Indica que se confirmó la entrada
        self.destroy()  # Cierra la ventana


def disparar(juego,tablero,turn,player,b):
    coordenada = simpledialog.askstring(f"Disparar J{player}", "Ingrese una coordenada (A-J 0-9):")
    if coordenada is None:
        messagebox.showwarning("Error", "No se ingreso valor")
        return turn,b
    elif coordenada.lower() and re.match(patron, coordenada):
        #Envia el string de la coordenada a la funcion disparar del objeto de clase Tablero en el modulo database y devuelve un booleano
        bomba = tablero.disparar(coordenada)
        tableroApi =  "tablero_aliado" if tablero == "tablero1" else "tablero_enemigo"
        cl.actualizarApi(coordenada,tableroApi)
        if bomba:
            juego.turtle.color("Red")
            juego.mover_a_casilla(coordenada)
            juego.dibujar_cuadrado(25)
            if b == 1:
                messagebox.showinfo("GG!", f"Felicidades P{player}, haz destruido todos los barcos del enemigo")
                return 0,0
            else:
                messagebox.showinfo("HIT!", "Haz dado en el blanco! Dispara de nuevo")
            return turn,b-1

        elif bomba is None:
            messagebox.showwarning("Error", "Ya se disparo en esa casilla, pruebe otra")
            return turn,b

        elif not bomba:
            juego.turtle.color("White")
            juego.mover_a_casilla(coordenada)
            juego.dibujar_cuadrado(25)
            if player == 1:
                return turn+1,b
            
            elif player == 2:
                return turn-1,b

    else:
        messagebox.showwarning("Error", "Coordenada Invalida")
        print("Coordenada inválida.")
        return turn,b


