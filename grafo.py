# Nodo del grafo con su nombre y su lista de vecinos.
class Nodo:

    # Crea un nodo sin vecinos.
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.vecinos: list[Conexion] = []


# Conexión con peso entre dos nodos.
class Conexion:

    # Crea una conexión con origen, destino y peso.
    def __init__(self, origen: Nodo, destino: Nodo, peso: float) -> None:
        self.origen = origen
        self.destino = destino
        self.peso = peso


# Grafo ponderado no dirigido con el algoritmo de Dijkstra.
class Grafo:

    # Construye el grafo a partir de una lista de conexiones.
    def __init__(self, conexiones: list[tuple[str, str, float]]) -> None:
        self.nodos: dict[str, Nodo] = {}

        for origen, destino, peso in conexiones:
            self.agregar_conexion(origen, destino, peso)

    # Crea el nodo si no existe y lo regresa.
    def agregar_nodo(self, nombre: str) -> Nodo:
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

        return self.nodos[nombre]

    # Agrega una conexión en los dos sentidos.
    def agregar_conexion(
        self, nombre_origen: str, nombre_destino: str, peso: float
    ) -> None:
        nodo_origen = self.agregar_nodo(nombre_origen)
        nodo_destino = self.agregar_nodo(nombre_destino)

        nodo_origen.vecinos.append(Conexion(nodo_origen, nodo_destino, peso))
        nodo_destino.vecinos.append(Conexion(nodo_destino, nodo_origen, peso))

    # Busca recursivamente el nodo no visitado con menor distancia.
    def buscar_nodo_mas_cercano(
        self,
        distancias: dict[str, float],
        visitados: list[str],
        posicion: int = 0,
    ) -> str | None:
        nombres = list(self.nodos)

        if posicion == len(nombres):
            return None

        nombre_actual = nombres[posicion]
        siguiente_nodo = self.buscar_nodo_mas_cercano(
            distancias, visitados, posicion + 1
        )

        if nombre_actual in visitados:
            return siguiente_nodo

        if siguiente_nodo is None:
            return nombre_actual

        if distancias[nombre_actual] < distancias[siguiente_nodo]:
            return nombre_actual

        return siguiente_nodo

    # Reemplaza el ciclo principal de Dijkstra por recursividad.
    def buscar_ruta(
        self,
        destino: str,
        distancias: dict[str, float],
        anteriores: dict[str, str | None],
        visitados: list[str],
    ) -> None:
        nombre_actual = self.buscar_nodo_mas_cercano(distancias, visitados)

        if nombre_actual is None:
            return

        if distancias[nombre_actual] == float("inf"):
            return

        if nombre_actual == destino:
            return

        visitados.append(nombre_actual)

        for conexion in self.nodos[nombre_actual].vecinos:
            nombre_vecino = conexion.destino.nombre
            nueva_distancia = distancias[nombre_actual] + conexion.peso

            if nueva_distancia < distancias[nombre_vecino]:
                distancias[nombre_vecino] = nueva_distancia
                anteriores[nombre_vecino] = nombre_actual

        self.buscar_ruta(destino, distancias, anteriores, visitados)

    # Construye recursivamente la ruta del origen al destino.
    def construir_camino(
        self,
        anteriores: dict[str, str | None],
        actual: str | None,
        camino: list[str],
    ) -> list[str]:
        if actual is None:
            camino.reverse()
            return camino

        camino.append(actual)

        return self.construir_camino(anteriores, anteriores[actual], camino)

    # Regresa la distancia mínima y la ruta completa entre dos nodos.
    def dijkstra(self, inicio: str, destino: str) -> tuple[float, list[str]]:
        if inicio not in self.nodos:
            raise ValueError(f"El nodo '{inicio}' no existe.")

        if destino not in self.nodos:
            raise ValueError(f"El nodo '{destino}' no existe.")

        distancias: dict[str, float] = {}
        anteriores: dict[str, str | None] = {}
        visitados: list[str] = []

        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        distancias[inicio] = 0

        self.buscar_ruta(destino, distancias, anteriores, visitados)

        if distancias[destino] == float("inf"):
            return float("inf"), []

        camino = self.construir_camino(anteriores, destino, [])

        return distancias[destino], camino
