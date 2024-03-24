import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from PIL import Image

# CSS para personalizar colores
css_personalizado = """
<style>
    /* Fondo blanco */
    body {
        background-color: white;
    }
    /* Letras azules */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .st-bb,
    .st-bf,
    .st-bj,
    .st-ci {
        color: red;
    }
    /* Cajas de entrada con fondo verde */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: #90EE90;  /* Un verde claro */
    }
</style>
"""
st.markdown(css_personalizado, unsafe_allow_html=True)

# Asegúrate de reemplazar 'path/to/your/logo.png' con la ruta real a tu imagen.
logo_path = 'logo.webp'
st.image(logo_path, caption='AgroDataHelper', width=400)


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

 # Título de la aplicación
st.title('AgroDataHelper - Asistente de Captura de Datos Agropecuarios')
st.header("Bienvenido al Asistente de Captura de Datos Agropecuarios")
st.write("Seleccione la opción que desea utilizar para comenzar.")

# Inicializa DataFrames vacíos para cultivos y ganado
df_cultivos = pd.DataFrame(columns=["Campo", "Tamaño (hectáreas)", "Tipo de Cultivo", "Rendimiento"])
df_ganado = pd.DataFrame(columns=["Tipo de Ganado", "Número de Cabezas", "Salud"])

# Sección de captura de datos para cultivos
st.header('Datos de Cultivos')
# Inicia un contenedor para el formulario de cultivos
with st.form("form_cultivos"):
    st.write("Datos de Cultivos")
    campo = st.text_input("Nombre del Campo")
    tamaño_hectareas = st.number_input("Tamaño del campo (hectáreas)", min_value=0.0, format="%f")
    tipo_cultivo = st.text_input("Tipo de Cultivo")
    rendimiento = st.number_input("Rendimiento (toneladas/hectárea)", min_value=0.0, format="%f")
    submit_cultivos = st.form_submit_button("Agregar Cultivo")

# Agrega datos al DataFrame de cultivos si el formulario de cultivos se envía
if submit_cultivos:
    nuevo_registro_cultivo = pd.DataFrame({"Campo": [campo], "Tamaño (hectáreas)": [tamaño_hectareas], "Tipo de Cultivo": [tipo_cultivo], "Rendimiento": [rendimiento]})
    df_cultivos = pd.concat([df_cultivos, nuevo_registro_cultivo], ignore_index=True)
    st.success("Datos de cultivo agregados exitosamente!")
    
# Inicia un contenedor para el formulario de ganado
with st.form("form_ganado"):
    st.write("Datos de Ganado")
    tipo_ganado = st.text_input("Tipo de Ganado")
    numero_cabezas = st.number_input("Número de cabezas de ganado", min_value=0, format="%d")
    salud_ganado = st.selectbox("Salud del Ganado", ["Buena", "Regular", "Mala"])
    submit_ganado = st.form_submit_button("Agregar Ganado")

# Agrega datos al DataFrame de ganado si el formulario de ganado se envía
if submit_ganado:
    nuevo_registro_ganado = pd.DataFrame({"Tipo de Ganado": [tipo_ganado], "Número de Cabezas": [numero_cabezas], "Salud": [salud_ganado]})
    df_ganado = pd.concat([df_ganado, nuevo_registro_ganado], ignore_index=True)
    st.success("Datos de ganado agregados exitosamente!")

# Opción para seleccionar el tipo de análisis o visualización
tipo_analisis = st.sidebar.selectbox("Selecciona el tipo de análisis:",
                                     ("Estadísticas Descriptivas", "Visualización de Datos"))

if tipo_analisis == "Estadísticas Descriptivas":
    st.subheader("Estadísticas Descriptivas")
    # Suponiendo que df_cultivos es tu DataFrame para los datos de cultivos
    if st.button('Mostrar Estadísticas Descriptivas de Cultivos'):
        st.write(df_cultivos.describe())

    if st.button('Mostrar Estadísticas Descriptivas de Ganado'):
        st.write(df_ganado.describe(include='all'))

elif tipo_analisis == "Visualización de Datos":
    st.subheader("Visualización de Datos")

    if st.button('Visualizar Rendimiento de Cultivos'):

        # Visualización para el DataFrame de cultivos: Histograma de Rendimiento
        plt.figure(figsize=(10, 6))
        plt.hist(df_cultivos['Rendimiento'], bins=10, color='skyblue', edgecolor='black')
        plt.title('Distribución del Rendimiento de los Cultivos')
        plt.xlabel('Rendimiento (toneladas/hectárea)')
        plt.ylabel('Frecuencia')
        plt.grid(True)
        st.pyplot(plt)
        plt.show()
    
    if st.button('Visualizar Rendimiento de Ganado'):
        # Visualización para el DataFrame de ganado: Gráfico de Barras del Número de Cabezas por Tipo de Ganado
        plt.figure(figsize=(10, 6))
        plt.bar(df_ganado['Tipo de Ganado'], df_ganado['Número de Cabezas'], color='lightgreen', edgecolor='black')
        plt.title('Número de Cabezas de Ganado por Tipo')
        plt.xlabel('Tipo de Ganado')
        plt.ylabel('Número de Cabezas')
        plt.grid(axis='y')
        st.pyplot(plt)        
        plt.show()

csv_cultivos = convert_df_to_csv(df_cultivos)
csv_ganado = convert_df_to_csv(df_ganado)

st.download_button(
    label="Descargar datos de Cultivos como CSV",
    data=csv_cultivos,
    file_name='datos_cultivos.csv',
    mime='text/csv',
)

st.download_button(
    label="Descargar datos de Ganado como CSV",
    data=csv_ganado,
    file_name='datos_ganado.csv',
    mime='text/csv',
)