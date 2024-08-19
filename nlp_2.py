import os
from GoogleNews import GoogleNews
import pandas as pd
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
import streamlit as st
from dotenv import load_dotenv
# Cargar las variables de entorno desde el archivo .env



@st.cache_data(persist=True)
def modelo_2(sentimientos):
  load_dotenv()
  api_key = os.getenv("OPENAI_API_KEY")

  prompt = ChatPromptTemplate.from_messages([
  ("system", "eres un experto en analitica de datos\n"
  "realiza un analisis basado en la frecuencia de las emociones donde determines que tan positivo es la percepcion de la poblacion acerca de la ciudad\n"
  "este analisis va dirijido a la cadena de valor turistica de la ciudad, asi que genera insights que puedan ser de utilidad para este sector dada los sentimientos analiszados \n"
  "El analisis debe ser conciso y no tener mas de 200 palabras "),

  ("human", "analiza la siguiente lista de palabras:\n\"{text}\"")])

  llm = ChatOpenAI(api_key=api_key, model="gpt-4o-mini", temperature=0)
  output_parser = StrOutputParser()

  chain = (
      prompt
      | llm
      | output_parser
  )
  analisis = str()
  analisis = chain.invoke({"text": sentimientos})
  
  return analisis