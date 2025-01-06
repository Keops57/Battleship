import csv
import os
import config
import helpers as hp
import tkinter as tk
import client as cl
from tkinter import messagebox
import random

class Casilla:
    def __init__(self, coord,barco=False, hit=False):
        self.coord = coord
        self.barco = barco
        self.hit = hit

    def __str__(self):
        return f"{self.coord} {self.barco} {self.hit}"

    def to_dict(self):
        return {'coord': self.coord, 'barco': self.barco, 'hit': self.hit}
    
    def hit_status(self):
        return {'coord': self.coord, 'hit': self.hit}


# noinspection SpellCheckingInspection
class Tablero:
    casillas = []
    def __init__(self,nombre):
        self.nombre = nombre
        self.archivo = f"{nombre}.csv"
        self.crear_tablero()  # Crear el tablero al inicializar
        self.root = tk.Tk()
        self.turno = False
        self.nb = 17
        self.root.withdraw()  # Oculta la ventana principal

    def crear_tablero(self):
        """Crea un tablero de tamaño 10x10."""
        if os.path.exists(self.archivo):
            print("El tablero ya ha sido creado. Cargando desde el archivo CSV...")
            self.cargar_csv()
        else:
            self.casillas = []

            letras = "abcdefghij"  # Letras para las filas
            for letra in letras:
                for numero in range(0, 10):
                    coord = f"{letra}{numero}"
                    casilla = Casilla(coord) 
                    self.casillas.append(casilla)
            self.crear_csv()  # Guardar el tablero en un CSV

    def crear_csv(self):
        """Crea el tablero en un archivo CSV."""
        with open(self.archivo, mode='w', newline='\n', encoding='utf-8') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            writer.writerow(['coord', 'barco', 'hit'])  # Cabecera del CSV
            for casilla in self.casillas:
                writer.writerow([casilla.coord, casilla.barco, casilla.hit])

    def cargar_csv(self):
        """Cargar el tablero desde un archivo CSV."""

        casillas = []
        with open(config.DATABASE_PATH,newline='\n') as fichero:
            reader = csv.reader(fichero,delimiter=';')
            next(reader, None)
            for coord, barco, hit in reader:
                casilla = Casilla(coord, barco == 'True', hit == 'True')
                casillas.append(casilla)
                # print(casilla)
        self.casillas = casillas
        print(f"Tablero {self.nombre} cargado desde el archivo CSV.")

        # lista_dicts = [casilla.to_dict() for casilla in self.casillas]
        # # Verificar el resultado
        # for dic in lista_dicts:
        #     print(dic)

    def modificar(self, coord, hit):
        """Permite actualizar los contenidos del csv"""
        for casilla in self.casillas:
            if casilla.coord == coord:
                casilla.hit = hit  # Cambiar solo el estado de hit
                break
        self.guardar() 

    def guardar(self):
        """Guarda el tablero en un archivo CSV."""
        with open(self.archivo, mode='w', newline='\n', encoding='utf-8') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            writer.writerow(['coord', 'barco', 'hit'])  # Cabecera
            for casilla in self.casillas:
                writer.writerow([casilla.coord, casilla.barco, casilla.hit])
        print("Tablero guardado correctamente.")

    def disparar(self, casilla):
        for coord in self.casillas:
            if coord.coord == casilla:
                if not coord.hit:  # Verifica si no se ha disparado
                    coord.hit = True
                    self.modificar(coord.coord, coord.hit) # Actualiza el estado en el CSV
                    if coord.barco:  # Si hay un barco en la casilla
                        print("Rojo")
                        return True
                    else:
                        print("Blanco")
                        return False
                else:
                    print("Ya se disparó a esta coordenada, elija otra.")
                    return None
        return None

    def reset(self):
        """Este metodo reinicia el tablero (en el csv), colocando todas las casillas sin barco ni disparo previo"""
        for casilla in self.casillas:
            casilla.hit = False
            casilla.barco = False
        cl.resetearApi(self.nombre) 
        print("El tablero ha sido reiniciado.")
        self.guardar()

    def colocar_barcos(self):
        nb = 0
        while nb<5:
            if nb==0:
                barco = "Destroyer (2)"
                size = 1
            elif nb==1:
                barco = "Submarine (3)"
                size = 2
            elif nb==2:
                barco = "Cruiser (3)"
                size = 2
            elif nb==3:
                barco = "Battleship (4)"
                size = 3
            else:
                barco = "Carrier (5)"
                size = 4
            
            """Función para solicitar las coordenadas usando la ventana secundaria."""
            app = hp.V_de_Casillas(self.root, "BattleShip", f"Ingrese las Coord de Inicio y Final del {barco}",size)
            app.grab_set()  # Bloquea la interacción con otras ventanas hasta que se cierre esta
            self.root.wait_window(app)  # Espera a que se cierre la ventana

            if app.resultado == "y":
                valido = False
                cont_casilla = 0
                print(f"{app.cI} -> {app.cF}")
                for casilla in self.casillas:
                    if casilla.coord in app.casillas_a_marcar and not casilla.barco:
                        casilla.barco = True
                        cl.colocarBarcosApi(casilla.coord,self.nombre)
                        cont_casilla += 1
                        if cont_casilla == size+1:
                            valido = True
                            break
                    elif casilla.coord in app.casillas_a_marcar and casilla.barco:
                        casilla_repetida = casilla.coord
                        valido = False
                        messagebox.showerror("Error", f"La casilla {casilla_repetida} ya tiene un barco encima, coloque de nuevo el barco: ")
                        break

                if valido:
                    nb+=1
                    self.guardar()
    
            else:
                print("El usuario canceló la entrada.")
                return
            
    def colocar_barcos_aleatorio(self):
        nb = 0
        lNumeros = [str(x) for x in range(0, 10)]
        lLetras = ["a","b","c","d","e","f","g","h","i","j"]
        while nb<5:
            casillas_a_marcar = []
            if nb==0:
                barco = "Destroyer (2)"
                size = 1
            elif nb==1:
                barco = "Submarine (3)"
                size = 2
            elif nb==2:
                barco = "Cruiser (3)"
                size = 2
            elif nb==3:
                barco = "Battleship (4)"
                size = 3
            else:
                barco = "Carrier (5)"
                size = 4
            
            cInicio, cFinal = hp.colocador_de_barcos(size)

            if cInicio[0] == cFinal[0]:
                for i in range(int(cInicio[1]), int(cFinal[1]) + 1):
                    casillas_a_marcar.append(f"{cInicio[0]}{i}")
                    print("Coordenadas Validas")
                    print(f"Coordenadas Actuales: {casillas_a_marcar}")
                valid_group = True
            
            elif cInicio[1] == cFinal[1]:
                for i in range(ord(cInicio[0]) , ord(cFinal[0]) + 1):
                    casillas_a_marcar.append(f"{chr(i)}{cFinal[1]}")
                    print("Coordenadas Validas")
                    print(f"Coordenadas Actuales: {casillas_a_marcar}")
                valid_group = True

            if(valid_group):
                valido = False
                cont_casilla = 0
                print(f"{cInicio} -> {cFinal}")
                for casilla in self.casillas:
                    if casilla.coord in casillas_a_marcar and not casilla.barco:
                        cont_casilla += 1
                        if cont_casilla == size+1:
                            valido = True
                            break
                    elif casilla.coord in casillas_a_marcar and casilla.barco:
                        casilla_repetida = casilla.coord
                        valido = False
                        print(f"La casilla {casilla_repetida} ya tiene un barco encima, coloque de nuevo el barco")
                        break

                if valido:
                    for casilla in self.casillas:
                        if casilla.coord in casillas_a_marcar and not casilla.barco:
                            casilla.barco = True
                            cl.colocarBarcosApi(casilla.coord,self.nombre)
                            cont_casilla += 1
                            if cont_casilla == size+1:
                                break
                    nb+=1
                    self.guardar()