# Proyecto 3: Interfaz web con Streamlit para Dijkstra

**Materia:** Programación III — CUGDL, Universidad de Guadalajara
**Autor:** Axel Salvador Jimenez Lopez

## Descripción

Aplicación web en Python 3.10 o superior que continúa el Proyecto 2. Permite agregar conexiones de una red a `nodos.csv`, ver siempre la tabla de nodos actualizada y calcular la ruta más corta entre dos nodos con el algoritmo de Dijkstra, todo desde una interfaz hecha con Streamlit.

## Estructura

```
.
├── .streamlit/
│   └── config.toml    # Colores y tema de la aplicación
├── main.py            # Interfaz Streamlit
├── grafo.py           # Clases Nodo, Conexion y Grafo (Dijkstra)
├── io_handler.py      # Lectura, escritura y validación del CSV
├── nodos.csv          # Conexiones de la red
├── portada.png        # Imagen de portada
├── requirements.txt   # Dependencias (streamlit y herramientas de calidad)
└── README.md
```

## Ejecución

```powershell
py -m pip install -r requirements.txt
py -m streamlit run main.py
```

Se abre en el navegador, normalmente en `http://localhost:8501`. La primera vez Streamlit puede pedir un correo en la terminal; presiona Enter para omitirlo.

## Cómo funciona

- **Portada:** título, imagen y los tres pasos de uso.
- **Pestaña Agregar conexión:** formulario con origen, destino y peso. Si el peso es texto, está vacío o es negativo, muestra el error sin guardar nada.
- **Pestaña Calcular ruta más corta:** selectores de inicio y destino. Muestra el costo total, la secuencia de nodos y el grafo con la ruta resaltada.
- **Panel derecho:** tabla de conexiones y totales siempre visibles. Las conexiones nuevas aparecen arriba. Si una fila del CSV está dañada, se omite y se avisa.

## Formato de `nodos.csv`

```
Origen,Destino,Peso
A,B,4
A,C,2
```

## Calidad de código

```powershell
py -m flake8
py -m ruff check
py -m mypy --strict main.py grafo.py io_handler.py
```

Los tres comandos deben terminar sin advertencias.
