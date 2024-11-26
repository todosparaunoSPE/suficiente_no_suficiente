# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:02:04 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

# Title
st.title("Estado de Cuenta: PENSIONISSSTE")
st.write("**Trabajador:** Javier Horacio Pérez Ricárdez")
st.write("**Fecha:** al 31 de agosto de 2024")

# First table: Resumen General
st.subheader("RESUMEN GENERAL (del 01 de 09 de 2023 al 31 de 08 de 2024 (12 meses))")
data1 = {
    'Concepto': ['Ahorro para el retiro 92 y 97¹', 'Ahorro voluntario', 'Ahorro para la vivienda 92, 97 y FOVISSSTE 92², ³'],
    'Saldo anterior': [23649.52, 429.10, 66483.97],
    'Aportaciones': [0.00, 669.35, None],
    'Retiros': [0.00, 90.87, 4867.44],
    'Rendimientos': [2689.13, 81.80, None],
    'Comisiones': [124.95, 2.88, None],
    'Saldo Final': [26393.70, 1086.50, 71351.41]
}

df1 = pd.DataFrame(data1)

# Agregar fila TOTAL
total_row_1 = df1.iloc[0, 6] + df1.iloc[1, 6] + df1.iloc[2, 6]
df1.loc['TOTAL'] = ['TOTAL', 0, 0, 0, 0, 0, total_row_1]

st.dataframe(df1)

# Second table: Destino para la pensión
st.subheader("AL MOMENTO DE PENSIONARTE EL TOTAL DE ESTAS SUBCUENTAS SE DESTINA PARA TU PENSIÓN")
data2 = {
    'Concepto': ['IMSS, Cesantía y Vejez y Cuota Social', 'ISSSTE, Cesantía y Vejez y Cuota Social, Retiro, Cesantía y Vejez (RCV)', 'Ahorro FOVISSSTE 2008 2, 3'],
    'Saldo anterior': [58299.59, 54946.63, 18982.56],
    'Aportaciones': [0.00, 13290.27, None],
    'Retiros': [0.00, 0.00, 5774.79],
    'Rendimientos': [7067.97, 7651.66, None],
    'Comisiones': [307.81, 320.57, None],
    'Saldo final': [65019.75, 75567.99, 24757.35]
}

df2 = pd.DataFrame(data2)

# Agregar fila TOTAL
total_row_2 = df2.iloc[0, 6] + df2.iloc[1, 6] + df2.iloc[2, 6]
df2.loc['TOTAL'] = ['TOTAL', 0, 0, 0, 0, 0, total_row_2]

st.dataframe(df2)

# Third table: Detalle de saldo final
st.subheader("Conceptos y Saldos - Detalle de saldo final")
data3 = {
    'Concepto': [
        'IMSS 1997', 'ISSSTE 2008', 'Cesantía en edad avanzada y vejez IMSS', 'Cuota social IMSS',
        'Cesantía en edad avanzada y vejez ISSSTE', 'Cuota social ISSSTE', 'Bono de pensión', 'SAR IMSS 1992',
        'SAR ISSSTE 1992', 'Aportaciones voluntarias (corto plazo)', 'Complementarias de retiro', 'Ahorro a largo plazo',
        'Ahorro solidario', 'SAR INFONAVIT 1992', 'SAR FOVISSSTE 1992', 'INFONAVIT 1997', 'FOVISSSTE 2008'
    ],
    'Saldo': [
        26393.70, 9415.44, 59364.86, 5654.89, 43781.62, 8582.32, 0.00, 0.00, 0.00, 1086.50, 0.00, 0.00, 13788.61, 0.00, 0.00, 71351.41, 24757.35
    ]
}

df3 = pd.DataFrame(data3)
st.dataframe(df3)

# Display total
st.write("**TOTAL:** $264,176.69")