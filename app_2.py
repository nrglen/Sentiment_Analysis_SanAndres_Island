import streamlit as st
from datetime import datetime, timedelta
from DataPreparation import dataCollection
from nlp_1 import modelo
from nlp_2 import modelo_2
import numpy as np
"""""
headers = {
    "authorization": st.secrets["OPENAI_API_KEY"],
    "content-type": "application/json"
}"""""


st.title("Analizador de sentimientos sobre las ciudades turisticas de Colombia")
descripcion = '''
Se busca determinar la percepcion sobre las ciudades turisiticas de el pais a partir de noticias recientes arrojadas por la API de googleNews.
La descripcion de las noticias es analizada por un modelo NLP construido con langChain soportado por la API de OpenAI.
Este modelo clasifica las emociones mas importantes encontradas en las descripciones de las noticias dado una lista de emociones seleccionadas.
posterior a eso, se grafica la frecuencia de estas emociones en el total de las noticias encontradas y se realiza un analisis de estas emociones
y se generan insights importantes para la cadena de valor turistica de la ciudad

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

ciudad_seleccionada = st.write("Por favor seleccione la ciudad a analizar")
select = st.selectbox("Ciudades Capitales", ciudades)


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


sentimientos = modelo(contenido)

# Crear un diccionario vacío
frecuencias = {}

# Contar las palabras manualmente
for palabra in sentimientos:
    if palabra in frecuencias:
        frecuencias[palabra] += 1
    else:
        frecuencias[palabra] = 1

st.bar_chart(frecuencias)

analisis_interactivo = modelo_2(sentimientos)

# Cuadro de texto para mostrar información
st.text_area(f'Analisis de sentimientos sobre la ciudad de {select}:', value=analisis_interactivo, height=300)

st.write(contenido)

