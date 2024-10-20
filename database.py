import csv
import turtle
import os
import helpers as hp
import tkinter as tk
from tkinter import messagebox as MessageBox
from tkinter import simpledialog as SimpleDialog
import re

class Casilla:
    def __init__(self, coord):
        self.coord = coord
        self.barco = False
        self.hit = False

    def __str__(self):
        return f"({self.coord}) {self.barco} {self.hit}"

    def to_dict(self):
        return {'coord': self.coord, 'barco': self.barco, 'hit': self.hit}

class Tablero:     
    def __init__(self,nombre):
        self.casillas = []
        self.archivo = f"{nombre}.csv"
        self.crear_tablero()  # Crear el tablero al inicializar
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal

    def crear_csv(self):
        """Guarda el tablero en un archivo CSV."""
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

    def crear_tablero(self):
        """Crea un tablero de tamaño 10x10."""
        if os.path.exists(self.archivo):
            print("El tablero ya ha sido creado. Cargando desde el archivo CSV...")
            self.cargar_csv()
        else:
            letras = "abcdefghij"  # Letras para las filas
            for letra in letras:
                for numero in range(1, 11):
                    coord = f"{letra}{numero}"
                    self.casillas.append(Casilla(coord))
            self.crear_csv()  # Guardar el tablero en un CSV

    def modificar(self, coord, hit):
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
        print("El tablero ha sido reiniciado.")
        self.guardar()
        ventana = hp.V_de_Opcion(self.root,"Nuevo Juego","¿Desea Volver a Jugar?")
        ventana.wait_window()

        eleccion = ventana.resultado

        if eleccion == "y":
            nb = 0
            while(nb<17):
                key = True
                while key:
                    c_elegida = SimpleDialog.askstring("Colocar", f"Ingrese una coordenada para el barco {nb+1} (A-J 1-10):")
                    if c_elegida == None:
                        MessageBox.showwarning("Error", "No se ingreso valor")
                    elif c_elegida.lower() and re.match(hp.patron, c_elegida):
                        print(f"{c_elegida}  {nb}")
                        for casilla in self.casillas:
                            print(f"{c_elegida} = {casilla.coord}?")
                            if c_elegida == casilla.coord:
                                print("Eo")
                                casilla.barco = True
                                print(casilla)
                                break
                        key = False
                nb+=1
            self.guardar()

        else:
            return None


# Inicializar el tablero
tablero1 = Tablero("tablero_enemigo")
tablero2 = Tablero("tablero_aliado")
