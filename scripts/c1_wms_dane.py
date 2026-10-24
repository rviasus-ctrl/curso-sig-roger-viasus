
import requests
import xml.etree.ElementTree as ET

URL = (
    "https://geoportal.dane.gov.co/mparcgis/services/"
    "MGN2024/Serv_CapasMGN_2024/MapServer/WMSServer"
)

params = {
    "service": "WMS",
    "request": "GetCapabilities"
}

respuesta = requests.get(URL, params=params, timeout=60)
respuesta.raise_for_status()

raiz = ET.fromstring(respuesta.content)

ns = {"wms": "http://www.opengis.net/wms"}

capas = raiz.findall(".//wms:Capability/wms:Layer//wms:Layer", ns)

capas_publicadas = [
    capa for capa in capas
    if capa.find("wms:Name", ns) is not None
]

crs = {
    elemento.text.strip()
    for elemento in raiz.findall(".//wms:CRS", ns)
    if elemento.text
}

formatos = {
    elemento.text.strip()
    for elemento in raiz.findall(
        ".//wms:Capability/wms:Request/wms:GetMap/wms:Format",
        ns
    )
    if elemento.text
}

print("\nSERVICIO WMS DEL DANE - MGN 2024")
print("--------------------------------")
print("HTTP:", respuesta.status_code)
print("Versión:", raiz.attrib.get("version"))
print("Capas con nombre:", len(capas_publicadas))

print("\nCAPAS PUBLICADAS:")
for capa in capas_publicadas:
    nombre = capa.findtext("wms:Name", namespaces=ns)
    titulo = capa.findtext("wms:Title", namespaces=ns)
    print(f"- {nombre}: {titulo}")

print("\nSISTEMAS DE REFERENCIA (CRS):")
for codigo in sorted(crs):
    print("-", codigo)

print("\nFORMATOS GETMAP:")
for formato in sorted(formatos):
    print("-", formato)
