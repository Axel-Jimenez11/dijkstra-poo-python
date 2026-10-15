# Proyecto 1: Algoritmo de Dijkstra

**Materia:** Programación III — CUGDL, Universidad de Guadalajara
**Autor:** Axel Salvador Jimenez Lopez
**Fecha de creación:** 13 de octubre de 2026

## Descripción

Implementación en Python 3 del algoritmo de Dijkstra para encontrar la ruta más corta en un grafo ponderado no dirigido. El programa muestra la **distancia o costo total** y la **secuencia exacta de nodos** del recorrido entre un nodo origen y uno destino.

## Diseño (POO)

| Clase | Responsabilidad |
|---|---|
| `Nodo` | Guarda el nombre del nodo y su lista de vecinos. |
| `Conexion` | Representa una arista con origen, destino y peso. |
| `Grafo` | Construye el grafo, ejecuta Dijkstra y reconstruye la ruta. |

El ciclo principal de Dijkstra y la reconstrucción del camino se implementaron con **recursividad**:

- `buscar_nodo_mas_cercano`: encuentra el nodo no visitado con menor distancia.
- `buscar_ruta`: sustituye el `while` principal del algoritmo.
- `construir_camino`: arma la ruta desde el destino hasta el origen.

## Requisitos

- Python 3.x
- No requiere librerías externas.

## Ejecución

```bash
python dijkstra_recursivo.py
```

## Ejemplo

Grafo de prueba (`CONEXIONES_BASICAS`):

| Origen | Destino | Peso |
|---|---|---|
| A | B | 4 |
| A | C | 2 |
| B | C | 1 |
| B | D | 5 |
| C | D | 8 |
| C | E | 10 |
| D | E | 2 |
| D | F | 6 |
| E | F | 3 |

Salida esperada:

```
Camino minimo de A a F:
A -> C -> B -> D -> E -> F
Distancia/costo total: 13
```

## Personalización

Para usar otro grafo, edita la lista `CONEXIONES_BASICAS` y cambia los nodos en la llamada `grafo.dijkstra("A", "F")`.