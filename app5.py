# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:42:14 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Función para calcular el saldo futuro en la cuenta AFORE con interés compuesto
def calcular_saldo_futuro(saldo_inicial, tasa_rendimiento, años_restantes, aportaciones_mensuales):
    saldo_futuro = saldo_inicial * (1 + tasa_rendimiento)**años_restantes
    for i in range(int(años_restantes)):  # Convertir años_restantes a entero
        saldo_futuro += aportaciones_mensuales * 12 * (1 + tasa_rendimiento)**(años_restantes - i - 1)
    return saldo_futuro

# Función para calcular el ingreso mensual disponible tras la jubilación
def calcular_ingreso_mensual(saldo_futuro, años_vida_post_jubilacion):
    return saldo_futuro / (años_vida_post_jubilacion * 12)

# Configuración de la interfaz de usuario en Streamlit
st.title("¿Será suficiente tu pensión al momento del retiro?")

# Cargar el archivo Excel automáticamente desde el directorio donde está el script
file_path = "dataset.xlsx"

if os.path.exists(file_path):
    # Leer los datos del archivo Excel automáticamente
    df = pd.read_excel(file_path)
    
    # Limpiar los nombres de las columnas eliminando espacios adicionales
    df.columns = df.columns.str.strip()
    
    # Mostrar los nombres de las columnas con su número de columna
    st.write("Nombres de las columnas y su número de columna:")
    column_names_with_index = {i: col for i, col in enumerate(df.columns)}
    st.write(column_names_with_index)
    
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
            ingreso_mensual = calcular_ingreso_mensual(saldo_futuro, años_vida_post_jubilacion)

            if ingreso_mensual >= gasto_mensual_jubilacion:
                pensión_suficiente = "Suficiente"
            else:
                pensión_suficiente = "No suficiente"

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
                'Ingreso mensual estimado durante la jubilación': f"${ingreso_mensual:,.2f}",
                'Evaluación de la pensión': pensión_suficiente
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

        # Gráfico de barras dinámico con Plotly
        evaluacion_counts = df_filtrado['Evaluación de la pensión'].value_counts().reset_index()
        evaluacion_counts.columns = ['Evaluación', 'Número de Trabajadores']

        fig = px.bar(
            evaluacion_counts, 
            x='Evaluación', 
            y='Número de Trabajadores',
            color='Evaluación',
            labels={'Evaluación': 'Evaluación de la Pensión', 'Número de Trabajadores': 'Cantidad'},
            title="Distribución de Evaluación de la Pensión"
        )

        # Personalizar la visualización del gráfico para mostrar números enteros con separadores de miles
        fig.update_traces(texttemplate='%{y}', textposition='outside', hovertemplate='%{x}: %{y:,}')
        st.plotly_chart(fig)

        # Cálculo de datos para las etiquetas
        total_trabajadores = len(df_resultados)
        trabajadores_no_suficiente = len(df_resultados[df_resultados['Evaluación de la pensión'] == 'No suficiente'])
        trabajadores_suficiente = len(df_resultados[df_resultados['Evaluación de la pensión'] == 'Suficiente'])

        # Mostrar los resultados debajo del gráfico con separadores de miles
        st.write("### Resumen")
        st.write(f"1. **Número total de trabajadores:** {total_trabajadores:,}")
        st.write(f"2. **Trabajadores cuya pensión no será suficiente:** {trabajadores_no_suficiente:,}")
        st.write(f"3. **Trabajadores cuya pensión será suficiente:** {trabajadores_suficiente:,}")

    else:
        st.error("El archivo no contiene todas las columnas necesarias.")
else:
    st.error("El archivo dataset.xlsx no se encuentra en el directorio.")

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
        
st.sidebar.title("Ayuda")
st.sidebar.write("""  
### ¿Qué hace esta aplicación?  
Este simulador te ayuda a calcular si el saldo acumulado en tu cuenta AFORE será suficiente para cubrir tus necesidades durante la jubilación. Puedes cargar un archivo Excel con los datos de varios trabajadores y obtener los resultados de la simulación.  

### Funcionalidades principales:  
1. **Cálculo del saldo futuro en la cuenta AFORE**:  
   - Utiliza la fórmula de interés compuesto para proyectar el saldo al momento de la jubilación.  
   - Considera las aportaciones mensuales como un porcentaje del salario.  

2. **Cálculo del ingreso mensual post-jubilación**:  
   - Calcula el ingreso mensual disponible basado en el saldo acumulado y la esperanza de vida post-jubilación.  

3. **Evaluación de suficiencia de pensión**:  
   - Determina si el ingreso mensual estimado es suficiente para cubrir los gastos mensuales estimados durante la jubilación.  

4. **Visualización interactiva**:  
   - Filtrar los resultados por evaluación ("Suficiente" o "No suficiente").  
   - Ver un gráfico interactivo con la distribución de las evaluaciones.  

### ¿Cómo usarla?  
1. Sube un archivo Excel con las siguientes columnas:  
   - Edad actual del trabajador  
   - Años cotizados  
   - Saldo actual en la cuenta AFORE  
   - Salario mensual actual  
   - Edad de jubilación  
   - Gasto mensual estimado  
   - Tasa anual de rendimiento del AFORE  
   - Esperanza de vida postjubilación  
2. Observa los resultados y utiliza los filtros para analizar los datos.  
3. Explora el gráfico para entender la distribución de las evaluaciones de la pensión.  
""")        

# Espacio para el mensaje de copyright

st.sidebar.markdown("© 2024 Todos los derechos reservados.")