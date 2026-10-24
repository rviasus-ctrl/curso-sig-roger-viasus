
import requests

URL = (
    "https://services6.arcgis.com/"
    "Ex2fmFOuTOHRZtML/ArcGIS/rest/services/"
    "Veredas_Boyaca_2024/FeatureServer/0/query"
)

BASE = {
    "where": "1=1",
    "outFields": "NOMB_MPIO,NOMBRE_VER",
    "outSR": "4326",
    "f": "geojson",
}


def descargar_veredas(bloque):
    features = []
    offset = 0
    vueltas = 0

    print(f"\nCONSULTA CON BLOQUES DE {bloque} REGISTROS")
    print("-" * 48)

    while True:
        parametros = {
            **BASE,
            "resultOffset": offset,
            "resultRecordCount": bloque,
        }

        respuesta = requests.get(
            URL, params=parametros, timeout=30
        )
        respuesta.raise_for_status()

        datos = respuesta.json()

        if "error" in datos:
            raise RuntimeError(datos["error"])

        nuevos = datos.get("features", [])

        features.extend(nuevos)
        vueltas += 1

        print(
            f"Vuelta {vueltas}: offset {offset}, "
            f"+{len(nuevos)} registros "
            f"(total {len(features)})"
        )

        if len(nuevos) < bloque:
            break

        offset += bloque

    municipios = {
        entidad["properties"]["NOMB_MPIO"]
        for entidad in features
    }

    print("-" * 48)
    print("Total de veredas:", len(features))
    print("Municipios distintos:", len(municipios))
    print("Número de vueltas:", vueltas)

    return len(features), len(municipios), vueltas


# B2.1 y B2.2: bloques de 1000
resultado_1000 = descargar_veredas(1000)

# B2.3: bloques de 500
resultado_500 = descargar_veredas(500)

print("\nCOMPARACIÓN FINAL")
print("-" * 48)
print("Bloques de 1000:", resultado_1000)
print("Bloques de 500:", resultado_500)

if resultado_1000[0] == resultado_500[0]:
    print("Los dos tamaños de bloque recuperaron el mismo total.")
else:
    print("ADVERTENCIA: los totales son diferentes.")
