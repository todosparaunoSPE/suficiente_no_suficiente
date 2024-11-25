# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 09:13:31 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Configuración de la página: debe ser el primer comando
st.set_page_config(page_title="Mapa de Salarios por Estado", layout="wide")

# Datos de salarios mínimos por estado
data = {
    "Estado": [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
        "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", "Colima", 
        "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", 
        "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", 
        "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", 
        "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", 
        "Yucatán", "Zacatecas"
    ],
    "Salario Mínimo": [
        207.44, 260.34, 260.34, 207.44, 207.44, 207.44, 260.34, 207.44, 
        207.44, 207.44, 207.44, 207.44, 207.44, 207.44, 207.44, 207.44, 
        207.44, 207.44, 260.34, 207.44, 207.44, 207.44, 260.34, 207.44, 
        207.44, 260.34, 207.44, 207.44, 207.44, 207.44, 207.44
    ]
}

# Agregar salario faltante
faltante = 207.44  # Valor provisional
data["Salario Mínimo"].append(faltante)

# Verificar longitud de las listas
if len(data["Estado"]) != len(data["Salario Mínimo"]):
    raise ValueError(
        f"Longitudes diferentes: Estados ({len(data['Estado'])}) vs Salarios ({len(data['Salario Mínimo'])})"
    )

# Crear DataFrame
df = pd.DataFrame(data)

# Cargar archivo GeoJSON localmente
try:
    with open("mexico_states.geojson", "r", encoding="utf-8") as file:
        mexico_geojson = json.load(file)
except FileNotFoundError:
    st.error("Error: Archivo GeoJSON no encontrado. Asegúrate de que 'mexico_states.geojson' esté en el directorio.")
    mexico_geojson = None

# Título y descripción
st.title("Mapa Interactivo de Salarios Mínimos por Estado en México")
st.write("Este mapa muestra el salario mínimo promedio por estado en México.")

# Función 1: Filtrar por Rango de Salario Mínimo
salario_minimo_range = st.slider(
    "Selecciona el rango de salarios mínimos",
    min_value=df["Salario Mínimo"].min(),
    max_value=df["Salario Mínimo"].max(),
    value=(df["Salario Mínimo"].min(), df["Salario Mínimo"].max())
)

# Filtrar DataFrame según el rango seleccionado
df_filtered = df[
    (df["Salario Mínimo"] >= salario_minimo_range[0]) & 
    (df["Salario Mínimo"] <= salario_minimo_range[1])
]

# Mostrar tabla de salarios filtrados
st.write("### Tabla de Salarios Filtrados por Rango")
st.dataframe(df_filtered)

# Función 2: Gráfico de Barras para Comparación de Salarios
fig_bar = px.bar(
    df_filtered, 
    x="Estado", 
    y="Salario Mínimo", 
    color="Salario Mínimo", 
    labels={"Salario Mínimo": "Salario (MXN)", "Estado": "Estado"}, 
    title="Comparación de Salarios Mínimos por Estado"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Función 3: Estadísticas Descriptivas
st.write("### Estadísticas Descriptivas de los Salarios Mínimos")
st.write(df["Salario Mínimo"].describe())

# Función 4: Comparar Salarios de los Estados Más Altos y Bajos
highest_salary_state = df.loc[df["Salario Mínimo"].idxmax()]
lowest_salary_state = df.loc[df["Salario Mínimo"].idxmin()]
st.write(f"**Estado con el salario más alto**: {highest_salary_state['Estado']} - ${highest_salary_state['Salario Mínimo']}")
st.write(f"**Estado con el salario más bajo**: {lowest_salary_state['Estado']} - ${lowest_salary_state['Salario Mínimo']}")

# Función 5: Filtro de Estado Específico
estado_seleccionado = st.selectbox("Selecciona un Estado", df["Estado"])

# Mostrar información del estado seleccionado
if estado_seleccionado:
    estado_info = df[df["Estado"] == estado_seleccionado]
    salario_estado = estado_info["Salario Mínimo"].values[0]
    st.write(f"**Salario mínimo en {estado_seleccionado}**: ${salario_estado}")

# Crear mapa solo si el archivo GeoJSON se carga correctamente
if mexico_geojson:
    fig = px.choropleth(
        df_filtered,
        geojson=mexico_geojson,
        locations="Estado",
        featureidkey="properties.name",
        color="Salario Mínimo",
        color_continuous_scale="Viridis",
        hover_name="Estado",
        labels={"Salario Mínimo": "Salario (MXN)"}
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(
        title="Mapa de Salarios Mínimos por Estado en México",
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    # Mostrar el mapa
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No se pudo cargar el archivo GeoJSON. Verifica la ubicación del archivo o el acceso a internet.")