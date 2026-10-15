"""
Titulo: Proyecto 1: Algoritmo de Dijkstra
Nombre completo: Axel Salvador Jimenez Lopez
Fecha de cracion: 13 de octubre del 2026
Descripcion: Implementar en Python el algoritmo de Dijkstra para encontrar la ruta más corta en un grafo ponderado (ej. red de transporte, router de red o interacción entre nodos).
"""


class Nodo:

    # Crea un nodo con su nombre y su lista de vecinos.
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = []


class Conexion:

    # Crea una conexion con origen, destino y peso.
    def __init__(self, origen, destino, peso):
        self.origen = origen
        self.destino = destino
        self.peso = peso


class Grafo:

    # Recibe las conexiones y construye todos los nodos del grafo.
    def __init__(self, conexiones):
        self.nodos = {}

        for origen, destino, peso in conexiones:
            self.agregar_conexion(origen, destino, peso)

    # Crea un nodo si no existe y lo regresa.
    def agregar_nodo(self, nombre):
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

        return self.nodos[nombre]

    # Agrega una conexion en los dos sentidos.
    def agregar_conexion(self, nombre_origen, nombre_destino, peso):
        nodo_origen = self.agregar_nodo(nombre_origen)
        nodo_destino = self.agregar_nodo(nombre_destino)

        conexion_ida = Conexion(nodo_origen, nodo_destino, peso)
        conexion_regreso = Conexion(nodo_destino, nodo_origen, peso)

        nodo_origen.vecinos.append(conexion_ida)
        nodo_destino.vecinos.append(conexion_regreso)

    # Busca recursivamente el nodo no visitado con menor distancia.
    def buscar_nodo_mas_cercano(self, distancias, visitados, posicion=0):
        nombres = list(self.nodos)

        if posicion == len(nombres):
            return None

        nombre_actual = nombres[posicion]
        siguiente_nodo = self.buscar_nodo_mas_cercano(
            distancias,
            visitados,
            posicion + 1
        )

        if nombre_actual in visitados:
            return siguiente_nodo

        if siguiente_nodo is None:
            return nombre_actual

        if distancias[nombre_actual] < distancias[siguiente_nodo]:
            return nombre_actual

        return siguiente_nodo

    # Reemplaza el while principal de Dijkstra por recursividad.
    def buscar_ruta(self, destino, distancias, anteriores, visitados):
        nombre_actual = self.buscar_nodo_mas_cercano(
            distancias,
            visitados
        )

        if nombre_actual is None:
            return

        if distancias[nombre_actual] == float("inf"):
            return

        if nombre_actual == destino:
            return

        visitados.append(nombre_actual)
        nodo_actual = self.nodos[nombre_actual]

        for conexion in nodo_actual.vecinos:
            nombre_vecino = conexion.destino.nombre
            nueva_distancia = (
                distancias[nombre_actual] + conexion.peso
            )

            if nueva_distancia < distancias[nombre_vecino]:
                distancias[nombre_vecino] = nueva_distancia
                anteriores[nombre_vecino] = nombre_actual

        self.buscar_ruta(
            destino,
            distancias,
            anteriores,
            visitados
        )

    # Construye recursivamente la ruta desde el destino hasta el origen.
    def construir_camino(self, anteriores, actual, camino):
        if actual is None:
            camino.reverse()
            return camino

        camino.append(actual)
        siguiente = anteriores[actual]

        return self.construir_camino(
            anteriores,
            siguiente,
            camino
        )

    # Calcula la distancia minima y la ruta completa.
    def dijkstra(self, inicio, destino):
        if inicio not in self.nodos:
            raise ValueError(f"El nodo '{inicio}' no existe.")

        if destino not in self.nodos:
            raise ValueError(f"El nodo '{destino}' no existe.")

        distancias = {}
        anteriores = {}
        visitados = []

        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        distancias[inicio] = 0

        self.buscar_ruta(
            destino,
            distancias,
            anteriores,
            visitados
        )

        if distancias[destino] == float("inf"):
            return float("inf"), []

        camino = self.construir_camino(
            anteriores,
            destino,
            []
        )

        return distancias[destino], camino


# Lista de conexiones: nombre del origen, nombre del destino y peso.
CONEXIONES_BASICAS = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("D", "E", 2),
    ("D", "F", 6),
    ("E", "F", 3),
]


# Se crea el grafo usando la lista de conexiones.
grafo = Grafo(CONEXIONES_BASICAS)


# Se obtiene y se muestra la ruta minima de A hasta F.
costo, camino = grafo.dijkstra("A", "F")
print("Camino minimo de A a F:")
print(" -> ".join(camino))
print("Distancia/costo total:", costo)
