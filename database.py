import csv
import os

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
    def __init__(self):
        self.casillas = []
        self.archivo = "tablero.csv"
        self.crear_tablero()  # Crear el tablero al inicializar

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
                self.guardar()  # Guarda el estado del tablero después de la modificación
                return casilla

    def guardar(self):
        """Guarda el tablero en un archivo CSV."""
        with open(self.archivo, mode='w', newline='\n', encoding='utf-8') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            writer.writerow(['coord', 'barco', 'hit'])  # Cabecera del CSV
            for casilla in self.casillas:
                writer.writerow([casilla.coord, casilla.barco, casilla.hit])  # Escribe cada casilla

    def disparar(self, casilla):
        for coord in self.casillas:
            if coord.coord == casilla:
                if not coord.hit:  # Verifica si no se ha disparado
                    coord.hit = True
                    if coord.barco:  # Si hay un barco en la casilla
                        print("Rojo")
                        self.modificar(coord.coord, True)  # Actualiza el estado en el CSV
                        return True
                    else:
                        print("Blanco")
                        self.modificar(coord.coord, True)  # Actualiza el estado en el CSV
                        return False
                else:
                    print("Ya se disparó a esta coordenada, elija otra.")
                    return None
        return None

    def reset(self):
        for casilla in self.casillas:
            casilla.hit = False
            casilla.barco = False
        print("El tablero ha sido reiniciado.")

# Inicializar el tablero
tablero = Tablero()
