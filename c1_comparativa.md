
# C1 — Comparación de estándares de servicios geográficos

## 1. Objetivo

Comparar los estándares WMS, WFS, FeatureServer y OGC API Features mediante la consulta de servicios geográficos y el análisis de sus mecanismos de acceso, filtrado y paginación.

## 2. Tabla comparativa

| Tecnología | Qué entrega | Cómo se filtra | Cómo se pagina |
|---|---|---|---|
| WMS | Imágenes de mapas renderizados | Selección de capas (LAYERS), extensión geográfica (BBOX) y CRS | No aplica paginación de entidades |
| WFS | Geometrías vectoriales y atributos | BBOX y filtros espaciales o de atributos | startIndex y count en WFS 2.0 |
| FeatureServer (Esri) | Entidades vectoriales y atributos mediante REST y GeoJSON | where, outFields y filtros espaciales | resultOffset y resultRecordCount |
| OGC API Features | Entidades geográficas mediante REST y GeoJSON | bbox, datetime y filtros admitidos por el servicio | limit y enlaces next; offset cuando está implementado |

## 3. Servicio WMS del DANE

Servicio consultado: MGN 2024.

- Versión WMS: 1.3.0.
- Respuesta HTTP: 200.
- Capas con nombre: 10.
- CRS anunciados: CRS:84, EPSG:102100, EPSG:3857 y EPSG:4326.
- Formatos GetMap anunciados: 9.

Capas identificadas: Manzana, Sección Urbana, Sector Urbano, Sección Rural, Sector Rural, Clase, Zona Urbana, Municipio, Departamento y País.

La información se obtuvo mediante una solicitud GetCapabilities y se procesó con Python utilizando requests y ElementTree.

## 4. FeatureServer — Veredas de Boyacá

Se consultó el servicio Veredas_Boyaca_2024 mediante una solicitud REST con los parámetros where=1=1, outFields=*, resultRecordCount=3 y f=geojson.

La respuesta utiliza una estructura FeatureCollection con entidades Feature, geometrías y atributos.

En los registros consultados se identificaron campos como NOMB_MPIO, NOMBRE_VER, CODIGO_VER, NOM_DEP y AREA_HA.

La paginación de este servicio puede realizarse mediante resultOffset y resultRecordCount, como se comprobó anteriormente en el ejercicio B2.

## 5. OGC API Features — pygeoapi

Se consultó la colección obs de la demostración oficial de pygeoapi, solicitando tres entidades mediante limit=3.

Resultados observados:

- Colección: obs.
- numberMatched: 5.
- numberReturned: 3.
- Formato: GeoJSON.
- Paginación: enlace rel=next con offset=3 y limit=3.

La respuesta contiene enlaces que permiten navegar entre los recursos y continuar la consulta de entidades.

## 6. Comparación de resultados

WMS entrega representaciones cartográficas como imágenes, mientras que WFS, FeatureServer y OGC API Features permiten acceder a entidades vectoriales y sus atributos.

FeatureServer y OGC API Features utilizan rutas REST y pueden devolver información estructurada en GeoJSON. En los servicios examinados, FeatureServer permite controlar los bloques mediante resultOffset y resultRecordCount, mientras que pygeoapi proporciona enlaces de navegación y parámetros limit y offset.

Las diferencias observadas corresponden a las capacidades de los servicios consultados y no necesariamente a todas las implementaciones posibles de cada tecnología.

