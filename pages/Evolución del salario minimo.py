# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 08:39:09 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import plotly.express as px


# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Datos ficticios de evolución del salario mínimo
data = {
    "Año": list(range(2000, 2025)),
    "Salario Mínimo": [
        30.0, 32.0, 33.5, 35.0, 36.0, 38.0, 40.0, 43.0, 45.0, 48.0,
        50.5, 52.0, 55.0, 58.0, 60.0, 63.0, 70.0, 80.0, 88.0, 98.0,
        102.0, 120.0, 141.0, 172.0, 207.0
    ]
}

# Convertir datos en un DataFrame
df = pd.DataFrame(data)

# Configuración de la página de Streamlit
#st.set_page_config(page_title="Evolución Salarial", layout="wide")
st.title("Gráfico Interactivo de Evolución del Salario Mínimo")

# Barra lateral de ayuda
st.sidebar.header("Ayuda")
st.sidebar.write("""
    Este código muestra un gráfico interactivo de la evolución del salario mínimo en México entre 2000 y 2024.
    
    **¿Qué hace este código?**
    - Muestra un gráfico interactivo de la evolución del salario mínimo a lo largo de los años.
    - Puedes ajustar el rango de años de la gráfica usando el deslizador en la barra lateral.
    - El gráfico se genera dinámicamente y se actualiza según los años seleccionados.
    
    **Interacción:**
    - Usa el deslizador para seleccionar un rango de años.
    - El gráfico se actualizará para mostrar los datos del salario mínimo solo dentro del rango seleccionado.

    **Información adicional:**
    - Esta aplicación es solo un ejemplo y usa datos ficticios de la evolución salarial.
    - Puedes observar el salario mínimo en pesos mexicanos (MXN) en función de los años seleccionados.
    
    **Desarrollado por:**
    - Javier Horacio Pérez Ricárdez
    - © 2024 Todos los derechos reservados.
""")

# Filtros: Selección de rango de años
st.sidebar.header("Filtros")
min_year, max_year = st.sidebar.slider(
    "Selecciona el rango de años", 
    min_value=int(df["Año"].min()), 
    max_value=int(df["Año"].max()), 
    value=(2010, 2025)
)

# Filtrar datos según el rango de años seleccionado
filtered_data = df[(df["Año"] >= min_year) & (df["Año"] <= max_year)]

# Crear gráfico interactivo con Plotly
fig = px.line(
    filtered_data, 
    x="Año", 
    y="Salario Mínimo", 
    title="Evolución del Salario Mínimo en México",
    labels={"Año": "Año", "Salario Mínimo": "Salario (MXN)"},
    markers=True
)

fig.update_layout(
    xaxis_title="Año",
    yaxis_title="Salario Mínimo (MXN)",
    template="plotly_white"
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

# Mostrar datos filtrados
st.write("### Datos Filtrados")
st.dataframe(filtered_data)
