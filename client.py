import requests
import config as cf

# print("""Que tablero quiere trabajar?
# <1> Tablero aliado
# <2> Tablero enemigo""")
# op = int(input())

# tablero =  "tablero_aliado" if op == 1 else "tablero_enemigo"



def actualizarApi(casilla,tablero):
    data = {"hit": True}
    url = f"http://127.0.0.1:8000/tablero/{tablero}/casillas/{casilla}"


    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("Casilla modificada:", response.json())
    else:
        print("Error:", response.status_code, response.json())

def resetearApi(tablero):
    data = {"barco":False,"hit": False}
    url = f"http://127.0.0.1:8000/tablero/{tablero}/reset"

    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("Tablero Reseteado:", response.json())
    else:
        print("Error:", response.status_code, response.json())

def colocarBarcosApi(casilla,tablero):
    data = {"barco": True}
    url = f"http://127.0.0.1:8000/tablero/{tablero}/casillas/{casilla}/posicionar"
    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("Casilla modificada:", response.json())
    else:
        print("Error:", response.status_code, response.json())


def modificar_turnos(tablero,turno):
    url = f"{cf.BASE_URL}/turno/{tablero}"
    data = {"turno": turno}
    response = requests.put(url, json=data)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error al cambiar el turno:")
        print("Código de estado:", response.status_code)
        print("Respuesta:", response.json())
    
def obtener_turno(tablero):
    url = f"{cf.BASE_URL}/turno/{tablero}"

    response = requests.get(url)

    if response.status_code == 200:
        # Extrae el valor booleano del campo 'turno' en el JSON
        turno = response.json().get("turno")
        return turno
    else:
        print("Error al obtener el turno:")
        print("Código de estado:", response.status_code)
        print("Respuesta:", response.json())
        return None