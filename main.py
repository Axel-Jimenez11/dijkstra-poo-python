"""
Titulo: Proyecto 2: Persistencia, Archivos y Excepciones
Nombre completo: Axel Salvador Jimenez Lopez
Fecha de creación: 27 de octubre del 2026
Descripcion: Programa interactivo que guarda conexiones de una red en un
archivo CSV, carga el grafo desde ese archivo y calcula la ruta más corta
con el algoritmo de Dijkstra.
"""

from grafo import Grafo
from io_handler import (
    cargar_conexiones,
    formatear_peso,
    guardar_conexion,
    validar_nombre,
    validar_peso,
)


# Pide un nombre de nodo hasta que el usuario escriba uno válido.
def pedir_nombre(mensaje: str) -> str:
    while True:
        try:
            return validar_nombre(input(mensaje))
        except ValueError as error:
            # Entrada vacía.
            print(f"Dato inválido: {error}")


# Pide un peso hasta que el usuario escriba un número válido.
def pedir_peso() -> float:
    while True:
        try:
            return validar_peso(input("Peso: "))
        except ValueError as error:
            # Texto, número negativo o campo vacío.
            print(f"Dato inválido: {error}")


# Pide una conexión al usuario y la guarda en el CSV.
def agregar_conexion() -> None:
    origen = pedir_nombre("Nodo origen: ")
    destino = pedir_nombre("Nodo destino: ")

    if origen == destino:
        print("El origen y el destino deben ser nodos distintos.")
        return

    peso = pedir_peso()

    try:
        guardar_conexion(origen, destino, peso)
    except OSError as error:
        # El archivo está abierto en otro programa o no hay permisos.
        print(f"No se pudo guardar la conexión: {error}")
        return

    print(f"Conexión guardada: {origen} - {destino} ({formatear_peso(peso)})")


# Carga el grafo desde el CSV y muestra la ruta más corta.
def calcular_ruta() -> None:
    conexiones = cargar_conexiones()

    if not conexiones:
        print("No hay conexiones válidas. Agrega al menos una.")
        return

    grafo = Grafo(conexiones)
    print("Nodos disponibles:", ", ".join(grafo.nodos))

    inicio = pedir_nombre("Nodo de inicio: ")
    destino = pedir_nombre("Nodo de destino: ")

    try:
        costo, camino = grafo.dijkstra(inicio, destino)
    except ValueError as error:
        # El nodo escrito no existe en el grafo.
        print(error)
        return

    if not camino:
        print(f"No existe una ruta de {inicio} a {destino}.")
        return

    print(f"Camino minimo de {inicio} a {destino}:")
    print(" -> ".join(camino))
    print("Distancia/costo total:", formatear_peso(costo))


# Muestra el menú principal y ejecuta la opción elegida.
def main() -> None:
    opciones = {"1": agregar_conexion, "2": calcular_ruta}

    try:
        while True:
            print("\n1. Agregar conexión")
            print("2. Calcular ruta más corta")
            print("3. Salir")
            opcion = input("Elige una opción: ").strip()

            if opcion == "3":
                break

            accion = opciones.get(opcion)

            if accion is None:
                print("Opción inválida. Elige 1, 2 o 3.")
            else:
                accion()
    except (KeyboardInterrupt, EOFError):
        # El usuario cerró el programa con Ctrl + C o Ctrl + Z.
        print()

    print("Programa terminado.")


if __name__ == "__main__":
    main()
