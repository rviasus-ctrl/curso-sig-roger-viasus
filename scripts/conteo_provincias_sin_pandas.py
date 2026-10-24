
import json
from collections import Counter
from pathlib import Path

# Ruta del archivo GeoJSON
ruta = Path(__file__).resolve().parent.parent / "datos" / "provincias_boyaca.geojson"

# Leer los datos
with open(ruta, encoding="utf-8") as archivo:
    datos = json.load(archivo)

# Contar municipios por provincia
conteo = Counter(
    entidad["properties"]["provincia"]
    for entidad in datos["features"]
)

print("MUNICIPIOS POR PROVINCIA - BOYACÁ")
print("-" * 40)

for provincia, cantidad in conteo.most_common():
    print(f"{provincia:25} {cantidad}")

print("-" * 40)
print(f"Total de municipios: {sum(conteo.values())}")
print(f"Total de provincias: {len(conteo)}")

