import tkinter as tk
import database as db
import helpers as hp
import api as ap
import client as cl

class Juego:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal
        self.grid1 = hp.TurtleWindow("Tablero Aliado","#144c74")
        self.grid1.matriz(10)
        self.grid2 = hp.TurtleWindow("Tablero Enemigo","#ADD8E6")
        self.grid2.matriz(10)

    def jugar(self):
        tablero1 = ap.tablero_aliado
        tablero2 = ap.tablero_enemigo

        ventana = hp.V_de_Opcion(self.root,"Reinicio","¿Desea reiniciar el tablero?")
        ventana.wait_window()

        eleccion = ventana.resultado
        if eleccion == "y":
            tablero1.reset()
            tablero2.reset()
            key = False
            
        elif eleccion == "n":
            key = True

        else:
            key =True
        
        if not key:
            ventana = hp.V_de_Opcion(self.root,"Nuevo Juego","¿Desea Jugar?")
            ventana.wait_window()

            eleccion = ventana.resultado

            if eleccion == "y":
                tablero1.colocar_barcos()
                print("Listo Tablero 1")
                tablero2.colocar_barcos_aleatorio()
                print("Listo Tablero 2")
                key = True
                

            else:
                return

        for coord in tablero1.casillas:
            if coord.barco:
                self.grid1.turtle.color("Black")
                self.grid1.mover_a_casilla(coord.coord)
                self.grid1.dibujar_cuadrado(25)
                
        for coord in tablero2.casillas:
            if coord.barco:
                self.grid2.turtle.color("Black")
                self.grid2.mover_a_casilla(coord.coord)
                self.grid2.dibujar_cuadrado(25)
    

        ap.tablero_aliado.turno = True

        while ap.tablero_aliado.nb>0 and ap.tablero_enemigo.nb>0:
            if ap.tablero_aliado.turno:
                    turn = True
                    while turn:
                        turn,ap.tablero_aliado.nb = hp.disparar(self.grid2,tablero2,turn,1,ap.tablero_aliado.nb)
                    ap.tablero_aliado.turno = not cl.obtener_turno(ap.tablero_aliado.nombre)
                    ap.tablero_enemigo.turno = not cl.obtener_turno(ap.tablero_enemigo.nombre)
                    cl.modificar_turnos(ap.tablero_enemigo.nombre,True)

            elif ap.tablero_enemigo.turno:
                    turn = True
                    while turn:
                        turn,ap.tablero_enemigo.nb = hp.disparar(self.grid1,tablero1,turn,2,ap.tablero_enemigo.nb)
                    ap.tablero_aliado.turno = not cl.obtener_turno(ap.tablero_aliado.nombre)
                    ap.tablero_enemigo.turno = not cl.obtener_turno(ap.tablero_enemigo.nombre)
                    cl.modificar_turnos(ap.tablero_aliado.nombre,True)

        self.root.destroy()  # Cierra la ventana principal de Tkinter

# Ejecutar el juego
juego = Juego()