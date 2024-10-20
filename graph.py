from tkinter import *
import tkinter as tk
import re
import database as db
import helpers as hp
from tkinter import messagebox as MessageBox
from tkinter import simpledialog as SimpleDialog

class Juego:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal
        self.grid1 = hp.TurtleWindow("Tablero Enemigo","#144c74")
        self.grid1.matriz(10)
        self.grid2 = hp.TurtleWindow("Tablero Aliado","#ADD8E6")
        self.grid2.matriz(10)

    def jugar(self):
        tablero1 = db.tablero1
        tablero2 = db.tablero2

        ventana = hp.V_de_Opcion(self.root,"Reinicio","¿Desea reiniciar el tablero?")
        ventana.wait_window()

        eleccion = ventana.resultado
        if eleccion == "y":
            r = tablero1.reset()
            if r == None:
                key = False
            else:
                key = True

            
        elif eleccion == "n":
            key = True
        
        while key:
            ventana = hp.V_de_Opcion(self.root,"Disparo","¿Desea disparar?")
            ventana.wait_window()  # Espera a que el usuario elija una opción

            eleccion = ventana.resultado
            if eleccion == "y":
                coordenada = SimpleDialog.askstring("Disparar", "Ingrese una coordenada (A-J 1-10):")
                if coordenada == None:
                        MessageBox.showwarning("Error", "No se ingreso valor")
                elif coordenada.lower() and re.match(hp.patron, coordenada):
                    bomba = tablero1.disparar(coordenada)
                    if bomba == True:
                        self.grid1.turtle.color("Red")
                        self.grid1.mover_a_casilla(coordenada)
                        self.grid1.dibujar_cuadrado(25)
                    elif bomba == False:
                        self.grid1.turtle.color("White")
                        self.grid1.mover_a_casilla(coordenada)
                        self.grid1.dibujar_cuadrado(25)
                    elif bomba == None:
                        MessageBox.showwarning("Error", "Ya se disparo en esa casilla, pruebe otra")
                
                    

                else:
                    print("Coordenada inválida.")
            elif eleccion == "n":
                break

        self.root.destroy()  # Cierra la ventana principal de Tkinter

# Ejecutar el juego
juego = Juego()