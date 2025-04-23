
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

class ParcelaInfo(BaseModel):
    nombre: str
    fecha: str  # "YYYY-MM-DD"

@app.get("/")
def root():
    return {"message": "Agronimus API running"}

@app.get("/logo")
def get_logo():
    return FileResponse("static/logo_agronimus.png", media_type="image/png")

@app.post("/generar-informe")
def generar_informe(parcela: ParcelaInfo):
    # Cargar datos
    nombre = parcela.nombre.strip()
    fecha = pd.to_datetime(parcela.fecha)
    df_ndvi = pd.read_csv("data/NDVI_153T.csv", parse_dates=["fecha"])
    df_ndwi = pd.read_csv("data/NDWI_153T.csv", parse_dates=["fecha"])
    df_parcelas = pd.read_excel("data/Plantilla_parcelas.xlsx")

    # Filtrar NDVI/NDWI por fecha
    actual_ndvi = df_ndvi[df_ndvi["fecha"] == fecha]["valor"].values[0]
    anterior_ndvi = df_ndvi[df_ndvi["fecha"] == fecha - pd.Timedelta(days=15)]["valor"].values[0]
    ndvi_variacion = round(((actual_ndvi - anterior_ndvi) / anterior_ndvi) * 100, 2)

    actual_ndwi = df_ndwi[df_ndwi["fecha"] == fecha]["valor"].values[0]
    anterior_ndwi = df_ndwi[df_ndwi["fecha"] == fecha - pd.Timedelta(days=15)]["valor"].values[0]
    ndwi_variacion = round(((actual_ndwi - anterior_ndwi) / anterior_ndwi) * 100, 2)

    # Crear informe en texto
    informe = f"""
    Informe Agronimus para la parcela {nombre}
    Fecha de análisis: {fecha.date()}
    -----------------------------------------
    Índice de Vigor (NDVI): {actual_ndvi} ({ndvi_variacion}% respecto a hace 15 días)
    Contenido hídrico (NDWI): {actual_ndwi} ({ndwi_variacion}% respecto a hace 15 días)

    Interpretación:
    - El vigor muestra una variación del {ndvi_variacion}%
    - El contenido hídrico muestra una variación del {ndwi_variacion}%

    Recomendaciones:
    - Revisar en campo si hay signos de estrés hídrico o vegetativo
    - Comparar con NDVI óptimo según la fenología del cultivo
    """

    output_path = f"Informe_{nombre.replace(' ', '_')}.txt"
    with open(output_path, "w") as f:
        f.write(informe)

    return FileResponse(output_path, media_type="text/plain", filename=output_path)
