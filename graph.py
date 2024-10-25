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
        self.grid1 = hp.TurtleWindow("Tablero Aliado","#144c74")
        self.grid1.matriz(10)
        self.grid2 = hp.TurtleWindow("Tablero Enemigo","#ADD8E6")
        self.grid2.matriz(10)

    def jugar(self):
        tablero1 = db.tablero1
        tablero2 = db.tablero2

        ventana = hp.V_de_Opcion(self.root,"Reinicio","¿Desea reiniciar el tablero?")
        ventana.wait_window()

        eleccion = ventana.resultado
        if eleccion == "y":
            tablero1.reset()
            tablero2.reset()
            key = False
            
        elif eleccion == "n":
            key = True
        
        if key == False:
            ventana = hp.V_de_Opcion(self.root,"Nuevo Juego","¿Desea Jugar?")
            ventana.wait_window()

            eleccion = ventana.resultado

            if eleccion == "y":
                tablero1.colocar_barcos()
                tablero2.colocar_barcos()
                key = True
                

            else:
                pass

        for coord in tablero1.casillas:
            if coord.barco == True:
                self.grid1.turtle.color("Black")
                self.grid1.mover_a_casilla(coord.coord)
                self.grid1.dibujar_cuadrado(25)
        for coord in tablero2.casillas:
            if coord.barco == True:
                self.grid2.turtle.color("Black")
                self.grid2.mover_a_casilla(coord.coord)
                self.grid2.dibujar_cuadrado(25)
    

        turn = 1
        b1,b2 = 17,17
        while b1>0 and b2>0:
            print(f"{b1} {b2}")
            if turn == 1:
                    turn,b1 = hp.disparar(self.grid2,tablero2,turn,1,b1)
            elif turn == 2:
                    turn,b2 = hp.disparar(self.grid1,tablero1,turn,2,b2)         

        self.root.destroy()  # Cierra la ventana principal de Tkinter

# Ejecutar el juego
juego = Juego()