"""
Titulo: Proyecto 3: Interfaz web con Streamlit para el algoritmo de Dijkstra
Nombre completo: Axel Salvador Jimenez Lopez
Fecha de creación: 12 de noviembre del 2026
Descripcion: Aplicación web que continúa el Proyecto 2. Permite agregar
conexiones a nodos.csv, ver la tabla de nodos siempre actualizada y calcular
la ruta más corta con el algoritmo de Dijkstra desde una interfaz Streamlit.
"""

from itertools import pairwise
from pathlib import Path

import streamlit as st

from grafo import Grafo
from io_handler import (
    Arista,
    cargar_conexiones,
    formatear_peso,
    guardar_conexion,
    validar_nombre,
    validar_peso,
)

RUTA_PORTADA = Path(__file__).parent / "portada.png"

PASOS = [
    ("1. Agrega", "Captura origen, destino y peso de cada conexión."),
    ("2. Se guarda", "Cada dato válido se escribe en nodos.csv."),
    ("3. Calcula", "Elige inicio y destino para ver la ruta más corta."),
]

ESTILOS = """
<style>
.block-container {padding-top: 2.5rem; max-width: 1300px;}
h1 {font-weight: 800; letter-spacing: -0.02em;}
.etiqueta {color: #B45309; font-weight: 700; font-size: 0.85rem;
    letter-spacing: 0.1em;}
.paso {background: #FFFFFF; border: 1px solid #CFE3DF;
    border-top: 4px solid #F59E0B; border-radius: 12px;
    padding: 14px 16px; height: 100%;}
.paso b {color: #0F766E;}
.paso span {color: #35504E; font-size: 0.95rem;}
</style>
"""

ESTILO_NODO = (
    'node [shape=circle, style=filled, fillcolor="#E3F1EE", '
    'color="#0F766E", fontcolor="#0B2B2A"];'
)
ESTILO_ARISTA = 'edge [color="#7FAFA9", fontcolor="#35504E"];'
ESTILO_RUTA = 'color="#F59E0B", penwidth=3'


# Aplica los estilos personalizados de la página.
def aplicar_estilos() -> None:
    st.markdown(ESTILOS, unsafe_allow_html=True)


# Muestra el título, la imagen y los pasos de uso del proyecto.
def mostrar_portada() -> None:
    columna_texto, columna_imagen = st.columns(
        [3, 2], gap="large", vertical_alignment="center"
    )

    with columna_texto:
        st.markdown(
            '<div class="etiqueta">PROGRAMACIÓN III · PROYECTO 3</div>',
            unsafe_allow_html=True,
        )
        st.title("Rutas más cortas con Dijkstra")
        st.write(
            "Captura las conexiones de una red, guárdalas en nodos.csv "
            "y calcula el camino de menor costo entre dos nodos."
        )

    with columna_imagen:
        if RUTA_PORTADA.exists():
            st.image(str(RUTA_PORTADA))

    for columna, (titulo, texto) in zip(st.columns(3), PASOS):
        columna.markdown(
            f'<div class="paso"><b>{titulo}</b><br><span>{texto}</span></div>',
            unsafe_allow_html=True,
        )


# Escapa las comillas de un nombre para usarlo dentro del código DOT.
def comillas(nombre: str) -> str:
    return '"' + nombre.replace('"', '\\"') + '"'


# Construye el código DOT del grafo y resalta la ruta indicada.
def construir_dot(conexiones: list[Arista], camino: list[str]) -> str:
    tramos = {frozenset(par) for par in pairwise(camino)}
    lineas = ["graph G {", "bgcolor=transparent;", ESTILO_NODO, ESTILO_ARISTA]

    for nombre in camino:
        lineas.append(
            f'{comillas(nombre)} [fillcolor="#FBBF24", color="#B45309"];'
        )

    for origen, destino, peso in conexiones:
        atributos = f'label="{formatear_peso(peso)}"'

        if frozenset((origen, destino)) in tramos:
            atributos += ", " + ESTILO_RUTA

        lineas.append(
            f"{comillas(origen)} -- {comillas(destino)} [{atributos}];"
        )

    lineas.append("}")

    return "\n".join(lineas)


# Valida los campos del formulario y guarda la conexión en el CSV.
def guardar_desde_formulario() -> None:
    try:
        origen = validar_nombre(st.session_state["campo_origen"])
        destino = validar_nombre(st.session_state["campo_destino"])
        peso = validar_peso(st.session_state["campo_peso"])
    except ValueError as error:
        # Campo vacío, peso con texto o número negativo.
        st.session_state["mensaje"] = ("error", f"Dato inválido: {error}")
        return

    if origen == destino:
        st.session_state["mensaje"] = (
            "error",
            "El origen y el destino deben ser nodos distintos.",
        )
        return

    try:
        guardar_conexion(origen, destino, peso)
    except OSError as error:
        # El archivo está abierto en otro programa o no hay permisos.
        st.session_state["mensaje"] = (
            "error",
            f"No se pudo guardar la conexión: {error}",
        )
        return

    st.session_state["mensaje"] = (
        "exito",
        f"Conexión guardada: {origen} - {destino} ({formatear_peso(peso)})",
    )
    st.session_state["campo_origen"] = ""
    st.session_state["campo_destino"] = ""
    st.session_state["campo_peso"] = ""


# Muestra el resultado del último intento de guardado.
def mostrar_mensaje() -> None:
    mensaje: tuple[str, str] | None = st.session_state.pop("mensaje", None)

    if mensaje is None:
        return

    tipo, texto = mensaje

    if tipo == "exito":
        st.success(texto)
    else:
        st.error(texto)


# Dibuja el formulario para agregar una conexión nueva.
def mostrar_formulario() -> None:
    with st.form("formulario_conexion", border=False):
        columnas = st.columns(3)
        columnas[0].text_input("Nodo origen", key="campo_origen")
        columnas[1].text_input("Nodo destino", key="campo_destino")
        columnas[2].text_input("Peso", key="campo_peso")
        st.form_submit_button(
            "Guardar conexión",
            type="primary",
            on_click=guardar_desde_formulario,
        )

    mostrar_mensaje()


# Dibuja los selectores y muestra la ruta más corta entre dos nodos.
def mostrar_calculo(conexiones: list[Arista]) -> None:
    if not conexiones:
        st.info("No hay conexiones válidas. Agrega al menos una.")
        return

    grafo = Grafo(conexiones)
    nombres = list(grafo.nodos)
    columnas = st.columns(2)
    inicio = columnas[0].selectbox("Nodo de inicio", nombres)
    destino = columnas[1].selectbox(
        "Nodo de destino", nombres, index=len(nombres) - 1
    )

    if inicio is None or destino is None:
        return

    try:
        costo, camino = grafo.dijkstra(inicio, destino)
    except ValueError as error:
        # El nodo ya no existe porque el CSV cambió durante la sesión.
        st.error(str(error))
        return

    if not camino:
        st.warning(f"No existe una ruta de {inicio} a {destino}.")
        return

    resultado = st.columns(2)
    resultado[0].metric("Costo total", formatear_peso(costo))
    resultado[1].metric("Nodos en la ruta", len(camino))
    st.success("Camino mínimo: " + " -> ".join(camino))
    st.graphviz_chart(construir_dot(conexiones, camino))


# Muestra la tabla de conexiones, sus totales y los avisos del CSV.
def mostrar_tabla(conexiones: list[Arista], avisos: list[str]) -> None:
    st.subheader("Nodos y conexiones")

    nodos = {nombre for arista in conexiones for nombre in arista[:2]}
    totales = st.columns(2)
    totales[0].metric("Nodos", len(nodos))
    totales[1].metric("Conexiones", len(conexiones))

    filas = [
        {"Origen": origen, "Destino": destino, "Peso": formatear_peso(peso)}
        for origen, destino, peso in reversed(conexiones)
    ]
    st.dataframe(filas, hide_index=True)
    st.caption("Las conexiones más recientes aparecen arriba.")

    if avisos:
        st.warning("\n\n".join(avisos))

    if conexiones:
        with st.expander("Ver grafo completo"):
            st.graphviz_chart(construir_dot(conexiones, []))


# Arma la página: portada, pestañas a la izquierda y tabla a la derecha.
def main() -> None:
    st.set_page_config(page_title="Dijkstra con Streamlit", layout="wide")
    aplicar_estilos()
    mostrar_portada()

    columna_izquierda, columna_derecha = st.columns([3, 2], gap="large")

    with columna_izquierda:
        pestana_agregar, pestana_ruta = st.tabs(
            ["Agregar conexión", "Calcular ruta más corta"]
        )

        with pestana_agregar:
            mostrar_formulario()

        conexiones, avisos = cargar_conexiones()

        with pestana_ruta:
            mostrar_calculo(conexiones)

    with columna_derecha:
        mostrar_tabla(conexiones, avisos)


if __name__ == "__main__":
    main()
