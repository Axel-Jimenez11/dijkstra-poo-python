# Proyecto 2: Persistencia, Archivos y Excepciones

**Materia:** Programación III — CUGDL, Universidad de Guadalajara
**Autor:** Axel Salvador Jimenez Lopez

## Descripción

Programa en Python 3.10 o superior que permite capturar por consola las conexiones de una red (nodo origen, nodo destino y peso), guardarlas en un archivo CSV, cargar el grafo desde ese archivo y calcular la ruta más corta con el algoritmo de Dijkstra del Proyecto 1.

## Estructura

```
.
├── main.py            # Menú interactivo y captura de datos
├── grafo.py           # Clases Nodo, Conexion y Grafo (Dijkstra)
├── io_handler.py      # Lectura, escritura y validación del CSV
├── nodos.csv          # Conexiones de la red
├── requirements.txt   # Dependencias de desarrollo (flake8, ruff)
└── README.md
```

## Ejecución

```powershell
py -m pip install -r requirements.txt
py main.py
```

Opciones del menú:

1. **Agregar conexión:** pide origen, destino y peso. Si el peso es texto, está vacío o es negativo, muestra el error y lo vuelve a pedir. Los datos válidos se agregan a `nodos.csv`.
2. **Calcular ruta más corta:** carga `nodos.csv`, pide un nodo de inicio y uno de destino, y muestra la ruta y el costo total.
3. **Salir.**

## Formato de `nodos.csv`

```
Origen,Destino,Peso
A,B,4
A,C,2
```

Si una fila está dañada (falta una columna, peso con texto o negativo), el programa la omite, avisa en qué línea ocurrió y continúa con las demás.

## Ejemplo

```
Camino minimo de A a F:
A -> C -> B -> D -> E -> F
Distancia/costo total: 13
```

## Calidad de código

```powershell
py -m flake8
py -m ruff check
```

Ambos comandos deben terminar sin advertencias.
