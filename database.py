import csv
import os
import helpers as hp
import tkinter as tk
from tkinter import messagebox

class Casilla:
    def __init__(self, coord):
        self.coord = coord
        self.barco = False
        self.hit = False

    def __str__(self):
        return f"({self.coord}) {self.barco} {self.hit}"

    def to_dict(self):
        return {'coord': self.coord, 'barco': self.barco, 'hit': self.hit}
    
    def hit_status(self):
        return {'coord': self.coord, 'hit': self.hit}


# noinspection SpellCheckingInspection
class Tablero:
    def __init__(self,nombre):
        self.nombre = nombre
        self.casillas = []
        self.archivo = f"{nombre}.csv"
        self.crear_tablero()  # Crear el tablero al inicializar
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal

    def crear_tablero(self):
        """Crea un tablero de tamaño 10x10."""
        if os.path.exists(self.archivo):
            print("El tablero ya ha sido creado. Cargando desde el archivo CSV...")
            self.cargar_csv()
        else:
            letras = "abcdefghij"  # Letras para las filas
            for letra in letras:
                for numero in range(0, 10):
                    coord = f"{letra}{numero}"
                    self.casillas.append(Casilla(coord))
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
        with open(self.archivo, mode='r', encoding='utf-8') as fichero:
            reader = csv.DictReader(fichero, delimiter=';')
            self.casillas = []
            for row in reader:
                casilla = Casilla(row['coord'])
                casilla.barco = row['barco'] == 'True'  # Convertir a booleano
                casilla.hit = row['hit'] == 'True'      # Convertir a booleano
                self.casillas.append(casilla)
            print("Tablero cargado desde el archivo CSV.")

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
        """Este método reinicia el tablero (en el csv), colocando todas las casillas sin barco ni disparo previo"""
        for casilla in self.casillas:
            casilla.hit = False
            casilla.barco = False
        print("El tablero ha sido reiniciado.")
        self.guardar()

    def colocar_barcos(self):
        nb = 0
        while nb<5:
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

# Inicializar el tablero
tablero1 = Tablero("tablero_aliado")
tablero2 = Tablero("tablero_enemigo")
