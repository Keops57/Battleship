from fastapi import FastAPI, HTTPException,Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import json
import database as db

app = FastAPI()

#region Icono

app.mount("/static", StaticFiles(directory="static"), name="static")


# Ruta para el favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

#endregion

#Instancias de los Tableros
tablero_aliado = db.Tablero("tablero_aliado")
tablero_enemigo = db.Tablero("tablero_enemigo")


# Mapear nombres de tableros a sus instancias
tableros = {
    "tablero_aliado": tablero_aliado,
    "tablero_enemigo": tablero_enemigo
}


@app.get("/")
def html():
    content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <a href='http://127.0.0.1:8000/tablero/tablero_aliado/casillas'>Tablero Aliado</a>
        <a href='http://127.0.0.1:8000/tablero/tablero_enemigo/casillas'>Tablero Enemigo</a>
    </head>
    </html>
    """
    return Response(content=content, media_type="text/html")

# Obtener Casillas
@app.get("/tablero/{nombre}/casillas", response_model=List[dict])
def obtener_casillas(nombre: str):
    if nombre not in tableros:
        raise HTTPException(status_code=404, detail=f"Tablero {nombre} no encontrado.")
    return [casilla.to_dict() for casilla in tableros[nombre].casillas]

@app.get("/tablero/{nombre}/casillas/{coord}", response_model=dict)
def obtener_casilla(nombre: str, coord: str):
    if nombre not in tableros:
        raise HTTPException(status_code=404, detail=f"Tablero {nombre} no encontrado.")
    for casilla in tableros[nombre].casillas:
        if casilla.coord == coord:
            return casilla.to_dict()
    raise HTTPException(status_code=404, detail=f"Casilla {coord} no encontrada en {nombre}.")

# Disparar Barcos
@app.put("/tablero/{nombre}/casillas/{coord}", response_model=dict)
def disparar_casilla(nombre: str, coord: str):
    if nombre not in tableros:
        raise HTTPException(status_code=404, detail=f"Tablero {nombre} no encontrado.")
    tablero = tableros[nombre]
    for casilla in tablero.casillas:
        if casilla.coord == coord:
            if casilla.hit == True:
                raise HTTPException(status_code=403, detail=f"Ya se le ha disparado a la  Casilla {coord} del {tablero}.")
            casilla.hit = True
            tablero.guardar()  # Actualizar el archivo CSV
            return casilla.to_dict()
    raise HTTPException(status_code=404, detail=f"Casilla {coord} no encontrada en {nombre}.")

# Resetear Tablero
@app.put("/tablero/{nombre}/reset", response_model=list[dict])
def reset_tablero(nombre: str):
    if nombre not in tableros:
        raise HTTPException(status_code=404, detail=f"Tablero {nombre} no encontrado.")
    tablero = tableros[nombre]
    for casilla in tablero.casillas:
        casilla.barco = False
        casilla.hit = False
        tablero.guardar()  # Actualizar el archivo CSV
    return [casilla.to_dict() for casilla in tableros[nombre].casillas]

# Colocar Barcos
@app.put("/tablero/{nombre}/casillas/{coord}/posicionar", response_model=dict)
def colocar_barcos(nombre: str, coord: str):
    if nombre not in tableros:
        raise HTTPException(status_code=404, detail=f"Tablero {nombre} no encontrado.")
    tablero = tableros[nombre]
    for casilla in tablero.casillas:
        if casilla.coord == coord:  
            casilla.barco = True
            tablero.guardar()  # Actualizar el archivo CSV
            return casilla.to_dict()
    raise HTTPException(status_code=404, detail=f"Casilla {coord} no encontrada en {nombre}.")

# Sistema de Turnos
@app.get("/tablero/{nombre}/turnos", response_model=dict)
def obtener_turnos(nombre: str):
    if nombre not in tableros:
        raise HTTPException(status_code=404, detail=f"Tablero {nombre} no encontrado.")
    tablero = tableros[nombre]

    
    return [casilla.to_dict() for casilla in tableros[nombre].casillas]



print("Servidor de la API...")