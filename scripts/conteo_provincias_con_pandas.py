
import json
import pandas as pd
from pathlib import Path

# Ruta del archivo GeoJSON
ruta = Path(__file__).resolve().parent.parent / "datos" / "provincias_boyaca.geojson"

# Leer el GeoJSON
with open(ruta, encoding="utf-8") as archivo:
    datos = json.load(archivo)

# Extraer atributos de los municipios
propiedades = [
    entidad["properties"]
    for entidad in datos["features"]
]

# Crear DataFrame
df = pd.DataFrame(propiedades)

# Agrupar y contar municipios por provincia
conteo = (
    df.groupby("provincia")
    .size()
    .sort_values(ascending=False)
)

print("MUNICIPIOS POR PROVINCIA - PANDAS")
print("-" * 45)
print(conteo.to_string())

print("-" * 45)
print(f"Total de municipios: {conteo.sum()}")
print(f"Total de provincias: {len(conteo)}")
