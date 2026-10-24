
from pathlib import Path

import geopandas as gpd
import requests

# Directorios del proyecto
BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / "datos"
SALIDAS = BASE.parent / "salidas"
SALIDAS.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# B1.1. Consultar veredas de Tunja mediante requests
# --------------------------------------------------

print("\nB1.1 - VEREDAS DE TUNJA (SERVICIO WEB)")

url = (
    "https://services6.arcgis.com/"
    "Ex2fmFOuTOHRZtML/ArcGIS/rest/services/"
    "Veredas_Boyaca_2024/FeatureServer/0/query"
)

params = {
    "where": "NOMB_MPIO = 'TUNJA'",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson",
}

try:
    respuesta = requests.get(url, params=params, timeout=30)
    respuesta.raise_for_status()
    contenido = respuesta.json()

    if "error" in contenido:
        raise ValueError(contenido["error"])

    tunja = gpd.GeoDataFrame.from_features(
        contenido["features"], crs="EPSG:4326"
    )

    print("Código HTTP:", respuesta.status_code)
    print("Veredas de Tunja:", len(tunja))

except (requests.RequestException, ValueError, KeyError) as error:
    print("Error al consultar el servicio:", error)

# --------------------------------------------------
# B1.2. Contar veredas por municipio
# --------------------------------------------------

print("\nB1.2 - DIEZ MUNICIPIOS CON MÁS VEREDAS")

ruta = DATOS / "veredas_boyaca.geojson"
veredas = gpd.read_file(ruta)

print("Total de registros:", len(veredas))

conteo = (
    veredas.groupby("NOMB_MPIO")
    .size()
    .sort_values(ascending=False)
)

print(conteo.head(10).to_string())

# --------------------------------------------------
# B1.3. Reproyectar y calcular superficies
# --------------------------------------------------

print("\nB1.3 - CINCO VEREDAS DE MAYOR SUPERFICIE")

veredas_m = veredas.to_crs("EPSG:9377")

veredas_m["area_ha"] = (
    veredas_m.geometry.area / 10000
)

columnas = ["NOMB_MPIO", "NOMBRE_VER", "area_ha"]

mayores = veredas_m.nlargest(5, "area_ha")

print(mayores[columnas].to_string(index=False))

# Exportar resultados a GeoPackage
salida = SALIDAS / "veredas_area.gpkg"

veredas_m.to_file(
    salida,
    driver="GPKG"
)

print("\nGeoPackage generado:", salida)
print("CRS de salida:", veredas_m.crs)
