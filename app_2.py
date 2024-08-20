import streamlit as st
from datetime import datetime, timedelta
from DataPreparation import dataCollection
from nlp_1 import modelo
from nlp_2 import modelo_2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.title("Análisis de Sentimientos y Clasificación de Noticias para el Turismo en San Andrés Islas")
descripcion = '''
Nuestra herramienta de análisis de sentimientos y clasificación de noticias está diseñada para comprender mejor cómo las noticias influyen en la percepción del turismo en San Andrés Islas, Colombia. Utilizando técnicas de Procesamiento de Lenguaje Natural (NLP), esta plataforma revisa automáticamente las emociones predominantes en las noticias, proporcionando insights clave que pueden ayudar a mejorar la competitividad turística del destino.
A través de la visualización interactiva, los usuarios pueden explorar cómo las emociones como optimismo, miedo o satisfacción afectan la percepción pública y podrán tomar decisiones informadas para fortalecer sus estrategias turísticas. \n
Además, esta aplicación es totalmente replicable para otros destinos turísticos. Simplemente ajusta los parámetros de búsqueda y utiliza la herramienta para analizar y comprender las emociones y tendencias en cualquier ciudad de interés de la lista desplegable, apoyando a los actores locales en la toma de decisiones estratégicas basadas en datos.
'''
st.markdown(descripcion)

ciudades = [
    "San Andrés islas",
    "Cartagena",
    "Bogotá",
    "Medellín",
    "Santa Marta",
    "Cali",
    "Barranquilla",
    "Villa de Leyva",
    "Pereira",
    "Bucaramanga"
]

ciudad_seleccionada = st.write("**Por favor seleccione la ciudad a analizar**")
select = st.selectbox("Ciudades Turisticas", ciudades)


# Definir la fecha de inicio (1 de enero del año actual)
fecha_inicio_calendario = datetime(datetime.now().year, 1, 1).date()

# Definir la fecha final (hoy)
fecha_final_calendario = datetime.now().date()

# Seleccionar la fecha inicial
fecha_inicial_seleccionada = st.date_input(
    "Selecciona la fecha de inicio para el analisis:",
    fecha_inicio_calendario,
    min_value=fecha_inicio_calendario,
    max_value=fecha_final_calendario
)

# Calcular la fecha final como 3 meses después de la fecha inicial seleccionada
fecha_final_max = fecha_inicial_seleccionada + timedelta(days=90)
# Ajustar la fecha final al máximo permitido entre la fecha calculada y la fecha actual
fecha_final_ajustada = min(fecha_final_max, fecha_final_calendario)

# Seleccionar la fecha final
fecha_final_seleccionada = st.date_input(
    "Fecha final para el analisis (máximo 3 meses después de la fecha de inicio):",
    fecha_final_ajustada,
    min_value=fecha_inicial_seleccionada,
    max_value=fecha_final_calendario
)

# Si la fecha final seleccionada supera la fecha actual, ajustarla automáticamente
if fecha_final_seleccionada > fecha_final_calendario:
    fecha_final_seleccionada = fecha_final_calendario

# Convertir la fecha a un objeto datetime
#fecha_inicio = datetime.strptime(fecha_inicial_seleccionada, '%Y-%m-%d')
#fecha_fin = datetime.strptime(fecha_final_seleccionada, '%Y-%m-%d')

# Convertir la fecha al formato DD/MM/YYYY
fecha_inicio_f = fecha_inicial_seleccionada.strftime('%d/%m/%Y')
fecha_fin_f = fecha_final_seleccionada.strftime('%d/%m/%Y')

contenido = dataCollection(fecha_inicio_f, fecha_fin_f, select)
df = pd.read_csv("Noticias.csv")

df = pd.read_csv('Noticias.csv')  # Ajusta el camino al archivo según corresponda

st.write("## Analisis exploratorio")
# Mostrar el DataFrame


# Análisis Exploratorio

# Frecuencia de publicaciones por medio
st.write("### Frecuencia de Publicaciones por Medio")
medio_counts = df['media'].value_counts()
st.bar_chart(medio_counts)

# Análisis de tipos de variables
st.write("### Tipos de Variables")
st.write(df.dtypes)


# Gráfico de la fecha de publicación
st.write("### Gráfico de Fechas de Publicación")
plt.figure(figsize=(10, 5))
sns.histplot(df['date'], kde=True)
plt.title('Distribución de Fechas de Publicación')
st.pyplot(plt)







sentimientos = modelo(contenido)

# Crear un diccionario vacío
frecuencias = {}

# Contar las palabras manualmente
for palabra in sentimientos:
    if palabra in frecuencias:
        frecuencias[palabra] += 1
    else:
        frecuencias[palabra] = 1
st.write("## Analisis de sentimientos")
st.bar_chart(frecuencias)

analisis_interactivo = modelo_2(sentimientos)

# Cuadro de texto para mostrar información
st.text_area(f'Analisis de sentimientos sobre la ciudad de {select}:', value=analisis_interactivo, height=300)

st.write("### Datos del DataFrame", df)
st.write("**Integrantes**: ")
st.write("Paola Lopez, Nadinson Ramos")

