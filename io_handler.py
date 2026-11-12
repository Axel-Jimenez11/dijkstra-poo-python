import csv
import math
from pathlib import Path

RUTA_CSV = Path(__file__).parent / "nodos.csv"
ENCABEZADOS = ["Origen", "Destino", "Peso"]

Arista = tuple[str, str, float]


# Regresa el nombre sin espacios sobrantes o lanza ValueError.
def validar_nombre(texto: str | None) -> str:
    if texto is None or not texto.strip():
        raise ValueError("el nombre del nodo no puede estar vacío.")

    return texto.strip()


# Convierte el texto a un peso válido (número finito y no negativo).
def validar_peso(texto: str | None) -> float:
    if texto is None or not texto.strip():
        raise ValueError("el peso no puede estar vacío.")

    try:
        peso = float(texto)
    except ValueError:
        raise ValueError(f"'{texto}' no es un número.") from None

    if not math.isfinite(peso) or peso < 0:
        raise ValueError("el peso debe ser un número mayor o igual a 0.")

    return peso


# Regresa el peso sin decimales cuando es un número entero.
def formatear_peso(peso: float) -> str:
    if peso.is_integer():
        return str(int(peso))

    return str(peso)


# Agrega una conexión al final del CSV y crea el encabezado si falta.
def guardar_conexion(
    origen: str, destino: str, peso: float, ruta: Path = RUTA_CSV
) -> None:
    necesita_encabezado = not ruta.exists() or ruta.stat().st_size == 0

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")

        if necesita_encabezado:
            escritor.writerow(ENCABEZADOS)

        escritor.writerow([origen, destino, formatear_peso(peso)])


# Valida una fila del CSV y la regresa como (origen, destino, peso).
def convertir_fila(fila: dict[str, str | None]) -> Arista:
    origen = validar_nombre(fila["Origen"])
    destino = validar_nombre(fila["Destino"])
    peso = validar_peso(fila["Peso"])

    return origen, destino, peso


# Lee el CSV fila por fila y regresa las conexiones válidas y los avisos.
def cargar_conexiones(
    ruta: Path = RUTA_CSV,
) -> tuple[list[Arista], list[str]]:
    conexiones: list[Arista] = []
    avisos: list[str] = []

    try:
        with open(ruta, newline="", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    conexiones.append(convertir_fila(fila))
                except KeyError as error:
                    # Falta una columna o encabezado en el CSV.
                    avisos.append(
                        f"Línea {lector.line_num} omitida: falta {error}."
                    )
                except ValueError as error:
                    # Dato corrupto, como un peso con texto o negativo.
                    avisos.append(
                        f"Línea {lector.line_num} omitida: {error}"
                    )
    except FileNotFoundError:
        # El archivo aún no existe porque no se ha guardado ninguna conexión.
        avisos.append(f"No se encontró el archivo '{ruta.name}'.")
    except (UnicodeDecodeError, csv.Error) as error:
        # El archivo está dañado y no se puede interpretar como CSV.
        avisos.append(f"No se pudo leer '{ruta.name}': {error}")

    return conexiones, avisos
