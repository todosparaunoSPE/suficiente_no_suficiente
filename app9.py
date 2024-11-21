# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 12:12:45 2024

@author: jperezr
"""


import streamlit as st
import pandas as pd
import plotly.express as px

# Función para calcular el saldo futuro en la cuenta AFORE con interés compuesto
def calcular_saldo_futuro(saldo_inicial, tasa_rendimiento, años_restantes, aportaciones_mensuales):
    saldo_futuro = saldo_inicial * (1 + tasa_rendimiento) ** años_restantes
    for i in range(int(años_restantes)):  # Aseguramos que años_restantes sea un entero
        saldo_futuro += aportaciones_mensuales * 12 * (1 + tasa_rendimiento) ** (años_restantes - i - 1)
    return saldo_futuro

# Función para calcular el ingreso mensual disponible tras la jubilación
def calcular_ingreso_mensual(saldo_futuro, años_vida_post_jubilacion):
    return saldo_futuro / (años_vida_post_jubilacion * 12) if años_vida_post_jubilacion > 0 else 0

# Configuración de la interfaz de usuario en Streamlit
st.title("¿Será suficiente tu pensión al momento del retiro?")

# Configuración de la barra lateral
st.sidebar.title("Opciones")

# Botón para descargar el archivo PDF
with open("modelo.pdf", "rb") as pdf_file:
    st.sidebar.download_button(
        label="Descargar modelo.pdf",
        data=pdf_file,
        file_name="modelo.pdf",
        mime="application/pdf"
    )  

# Agregar sección de ayuda en el sidebar
with st.sidebar:
    st.header("Ayuda")
    st.write("""  
    **Este es un simulador para estimar si tu pensión será suficiente para tu retiro.**

    1. **Sube un archivo de Excel** con los datos relevantes para la simulación. El archivo debe contener las siguientes columnas:
        - Edad actual del trabajador
        - Años cotizados
        - Saldo actual en la cuenta AFORE
        - Salario mensual actual
        - Edad de jubilación
        - Gasto mensual estimado
        - Tasa anual de rendimiento del AFORE
        - Esperanza de vida postjubilación

    2. El código calcula lo siguiente para cada trabajador:
        - El saldo acumulado estimado en la cuenta AFORE al momento de la jubilación.
        - El ingreso mensual disponible durante la jubilación.
        - El porcentaje del salario reemplazado por la pensión.
        - Una evaluación sobre si la pensión es **suficiente** o **no suficiente**.

    3. Los resultados de la simulación son mostrados en:
        - Un gráfico de barras de la distribución de la **Evaluación de la pensión** (si es suficiente o no).
        - Un gráfico de barras de la distribución por **Combinación de Evaluación y Estado de Jubilación** (por ejemplo, si la persona ha alcanzado la edad de jubilación o está en proceso).
    
    4. Puedes filtrar los resultados usando los **selectbox** o **multiselect** para visualizar solo las combinaciones deseadas.

    5. **Resumen de los resultados**:
        - El número total de trabajadores para cada categoría de evaluación.
        - El número total de trabajadores para cada combinación de evaluación y estado de jubilación.
    """)

# Cargar automáticamente el archivo Excel (dataset.xlsx)
file_path = "dataset.xlsx"
try:
    df = pd.read_excel(file_path)
    # Limpiar los nombres de las columnas eliminando espacios adicionales
    df.columns = df.columns.str.strip()

    # Asegúrate de que las columnas tienen los nombres correctos
    required_columns = ['Edad actual del trabajador', 'Años cotizados', 'Saldo actual en la cuenta AFORE', 
                        'Salario mensual actual', 'Edad de jubilación', 'Gasto mensual estimado',
                        'Tasa anual de rendimiento del AFORE', 'Esperanza de vida postjubilación']

    if all(col in df.columns for col in required_columns):
        st.write("Datos cargados exitosamente:")
        st.write(df)

        # Crear una lista para almacenar los resultados
        results = []

        # Iterar sobre las filas del archivo y realizar los cálculos
        for index, row in df.iterrows():
            edad_actual = row['Edad actual del trabajador']
            años_cotizados = row['Años cotizados']
            saldo_actual = row['Saldo actual en la cuenta AFORE']
            salario = row['Salario mensual actual']
            edad_jubilacion = row['Edad de jubilación']
            gasto_mensual_jubilacion = row['Gasto mensual estimado']
            tasa_rendimiento = row['Tasa anual de rendimiento del AFORE'] / 100
            esperanza_vida = row['Esperanza de vida postjubilación']

            años_restantes = edad_jubilacion - edad_actual
            años_vida_post_jubilacion = esperanza_vida - edad_jubilacion

            saldo_futuro = calcular_saldo_futuro(saldo_actual, tasa_rendimiento, años_restantes, salario * 0.10)

            # Verificar si los años restantes son mayores que cero
            if años_restantes > 0:
                ingreso_mensual_jubilacion = calcular_ingreso_mensual(saldo_futuro, años_vida_post_jubilacion)
                if salario > 0:
                    porcentaje_de_reemplazo = (ingreso_mensual_jubilacion / salario) * 100
                else:
                    porcentaje_de_reemplazo = 0
                pensión_suficiente = "Suficiente" if ingreso_mensual_jubilacion >= gasto_mensual_jubilacion else "No suficiente"
            else:
                ingreso_mensual_jubilacion = 0
                porcentaje_de_reemplazo = 0
                pensión_suficiente = "No suficiente"

            # Verificación de estado de jubilación
            if edad_actual >= edad_jubilacion:
                estado_jubilacion = "Ya ha alcanzado la edad de jubilación"
            else:
                estado_jubilacion = "Está en proceso de llegar a la jubilación"

            # Agregar los resultados al dataframe
            results.append({
                'Edad actual del trabajador': edad_actual,
                'Años cotizados': años_cotizados,
                'Saldo actual en la cuenta AFORE': saldo_actual,
                'Salario mensual actual': salario,
                'Edad de jubilación': edad_jubilacion,
                'Gasto mensual estimado': gasto_mensual_jubilacion,
                'Tasa anual de rendimiento del AFORE': tasa_rendimiento * 100,
                'Esperanza de vida postjubilación': esperanza_vida,
                'Saldo acumulado estimado en la cuenta AFORE al momento de la jubilación': f"${saldo_futuro:,.2f}",
                'Ingreso mensual estimado durante la jubilación': f"${ingreso_mensual_jubilacion:,.2f}",
                'Porcentaje del salario que se reemplaza': f"{porcentaje_de_reemplazo:.2f}%",
                'Evaluación de la pensión': pensión_suficiente,
                'Estado de jubilación': estado_jubilacion
            })

        df_resultados = pd.DataFrame(results)
        st.write("Resultados de la simulación de pensión:")
        st.write(df_resultados)

        # Filtro múltiple para la columna "Evaluación de la pensión"
        evaluacion_filter = st.multiselect(
            "Filtrar por Evaluación de la pensión", 
            options=df_resultados['Evaluación de la pensión'].unique(),
            default=df_resultados['Evaluación de la pensión'].unique()
        )
        df_filtrado = df_resultados[df_resultados['Evaluación de la pensión'].isin(evaluacion_filter)]

        st.write("Resultados filtrados:")
        st.write(df_filtrado)

        # Crear una columna combinada para las opciones de filtro
        df_filtrado['Combinación'] = df_filtrado['Evaluación de la pensión'] + ', ' + df_filtrado['Estado de jubilación']

        # Multiselect para filtrar por la combinación de "Evaluación de la pensión" y "Estado de Jubilación"
        combinacion_filter = st.multiselect(
            "Filtrar por Evaluación de la pensión y Estado de Jubilación",
            options=[
                "Suficiente, Está en proceso de llegar a la jubilación",
                "Suficiente, Ya ha alcanzado la edad de jubilación",
                "No suficiente, Está en proceso de llegar a la jubilación",
                "No suficiente, Ya ha alcanzado la edad de jubilación"
            ],
            default=[
                "Suficiente, Está en proceso de llegar a la jubilación",
                "Suficiente, Ya ha alcanzado la edad de jubilación",
                "No suficiente, Está en proceso de llegar a la jubilación",
                "No suficiente, Ya ha alcanzado la edad de jubilación"
            ]
        )
        df_filtrado_combinado = df_filtrado[df_filtrado['Combinación'].isin(combinacion_filter)]

        st.write("Resultados filtrados por Evaluación y Estado de Jubilación:")
        st.write(df_filtrado_combinado)

        # Gráfico de barras para "Distribución de la Evaluación de la Pensión"
        evaluacion_counts = df_filtrado['Evaluación de la pensión'].value_counts().reset_index()
        evaluacion_counts.columns = ['Evaluación', 'Número de Trabajadores']

        fig1 = px.bar(
            evaluacion_counts, 
            x='Evaluación', 
            y='Número de Trabajadores', 
            color='Evaluación',
            title="Distribución de la Evaluación de la Pensión"
        )
        st.plotly_chart(fig1)

        # Gráfico de barras para "Combinación de Evaluación y Estado de Jubilación"
        combinacion_counts = df_filtrado_combinado['Combinación'].value_counts().reset_index()
        combinacion_counts.columns = ['Combinación', 'Número de Trabajadores']

        fig2 = px.bar(
            combinacion_counts, 
            x='Combinación', 
            y='Número de Trabajadores', 
            color='Combinación',
            title="Distribución de la Evaluación y Estado de Jubilación"
        )
        st.plotly_chart(fig2)

        # Resumen de los resultados
        st.write("### Resumen de los resultados:")

        resumen_evaluacion = df_filtrado['Evaluación de la pensión'].value_counts().reset_index()
        resumen_evaluacion.columns = ['Evaluación', 'Número de Trabajadores']
        st.write("#### Resumen por Evaluación de la pensión:")
        st.write(resumen_evaluacion)

        resumen_combinacion = df_filtrado_combinado['Combinación'].value_counts().reset_index()
        resumen_combinacion.columns = ['Combinación', 'Número de Trabajadores']
        st.write("#### Resumen por Combinación de Evaluación y Estado de Jubilación:")
        st.write(resumen_combinacion)

    else:
        st.error("El archivo no contiene todas las columnas necesarias.")
except FileNotFoundError:
    st.error("El archivo 'dataset.xlsx' no se encuentra en el directorio.")


st.sidebar.markdown("Javier Horacio Pérez Ricárdez")
st.sidebar.markdown("© 2024 Todos los derechos reservados.")

