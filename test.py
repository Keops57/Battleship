from tkinter import *
import tkinter as tk
import re
from tkinter import messagebox as MessageBox
import turtle
from tkinter import simpledialog as SimpleDialog
import database as db
import graph as gr


class CenterWidgetMixin:
    def center(self):
        """Centra la ventana en la pantalla."""
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws - w) / 2)
        y = int((hs - h) / 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

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

        lista_numeros = [str(x) for x in range(1, 11)]
        lista_letras = ["a","b","c","d","e","f","g","h","i","j"]

        if not self.cI or not self.cF:
            MessageBox.showerror("Error", "Ambas coordenadas son obligatorias.")
            return  # No cerrar la ventana si los campos están vacíos
        
        
        if self.cI[0] == self.cF[0] and self.cI[1] in lista_numeros and self.cF[1] in lista_numeros:
            print([str(x) for x in range(0, 11)])
            valid = int(self.cF[1]) - int(self.cI[1]) 
            print(valid)

            if valid <=0:
                MessageBox.showerror("Error", "Posicionamiento invalido (Coloque las casillas de izq a der o de arriba a abajo)")
                return  # No cerrar la ventana si los campos están vacíos
            
            elif valid == self.lim:
                for i in range(int(self.cI[1]), int(self.cF[1]) + 1):
                    self.casillas_a_marcar.append(f"{self.cI[0]}{i}")
                print("Coordenadas Validas")
            
            else:
                MessageBox.showerror("Error", "Posicionamiento invalido")
                return  # No cerrar la ventana si los campos están vacíos


        elif self.cI[1] == self.cF[1] and self.cI[0] in lista_letras and self.cF[0] in lista_letras:

            valid = ord(self.cF[0]) - ord(self.cI[0]) 
            print(valid)

            if valid <=0:
                MessageBox.showerror("Error", "Posicionamiento invalido (Coloque las casillas de izq a der o de arriba a abajo)")
                return  # No cerrar la ventana si los campos están vacíos
            
            elif valid == self.lim:
                pass
                print("Coordenadas Validas")

            else:
                MessageBox.showerror("Error", "Posicionamiento invalido")
                return  # No cerrar la ventana si los campos están vacíos
            
        else:
            MessageBox.showerror("Error", "Posicionamiento invalido")
            return
        

        self.resultado = "y"  # Indica que se confirmó la entrada
        self.destroy()  # Cierra la ventana


def colocar_barcos(self):
    nb = 0
    while(nb<5):
        if nb==0:
            barco = "Peñero"
            size = 1
        elif nb==1:
            barco = "Submarino"
            size = 2
        elif nb==2:
            barco = "3Casillas"
            size = 2
        elif nb==3:
            barco = "4Casillas"
            size = 3
        else:
            barco = "Battleship"
            size = 4
        
        """Función para solicitar las coordenadas usando la ventana secundaria."""
        app = V_de_Casillas(root, "BattleShip", f"Ingrese las Coord de Inicio y Final del {barco}",size)
        app.grab_set()  # Bloquea la interacción con otras ventanas hasta que se cierre esta
        root.wait_window(app)  # Espera a que se cierre la ventana

        if app.resultado == "y":
            valido = True
            contCasilla = 0
            print(f"{app.cI} -> {app.cF}")
            for casilla in tablero.casillas:
                if casilla.coord in tablero.casillas and not casilla.barco:
                    casilla.barco = True
                    valido = True
                    contCasilla += 1
                    if contCasilla == size+1: 
                        break
                elif casilla.coord in tablero.casillas and casilla.barco:
                    casillaRepetida = casilla.coord
                    for casilla in tablero.casillas:
                        if casilla.coord in app.casillas_a_marcar:
                            casilla.barco =  False
                            valido = False
                    MessageBox.showerror("Error", f"La casilla {casillaRepetida} ya tiene un barco encima, coloque de nuevo el barco: ")
                    break

            if valido:
                nb+=1    
        else:
            print("El usuario canceló la entrada.")
            return


# Ventana principal oculta
root = tk.Tk()
root.withdraw()

if __name__ == "__main__":
    solicitar_coordenadas(db.tablero1)

#---------------------------------------------------------------------------


    

        