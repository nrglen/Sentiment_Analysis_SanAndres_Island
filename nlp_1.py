import os
from GoogleNews import GoogleNews
import pandas as pd
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
import streamlit as st
from dotenv import load_dotenv




#@st.cache_data(persist=True)
def modelo(contents):
  # Cargar las variables de entorno desde el archivo .env
  #load_dotenv()
  api_key = os.getenv("OPENAI_API_KEY")
  
  prompt = ChatPromptTemplate.from_messages([
  ("system", "You are a sentiment analyzer for news articles.\n"
  "Read the following news article and determine 3 most important emotions,dont explain the emotion, only put the word for them, dont put a period after the last emotion.\n"
  "analiza las emociones de cada noticia y clasificalas dentro de la lista de emociones: \n"
  "Optimismo, Emoción, crecimiento, seguridad,satisfacción, anticipation, admiración, anhelo, miedo, aburrimiento, economia "),

  ("human", "Analyze the following news article:\n\"{noticia}\"")])

  llm = ChatOpenAI(api_key=api_key, model="gpt-4o-mini", temperature=0)
  output_parser = StrOutputParser()

  chain = (
      {x: itemgetter(x) for x in ["noticia"]}
      | prompt
      | llm
      | output_parser
  )
  sentimientos = []
  for noticia in contents:
    #print(chain.invoke({"noticia": noticia}))
    sentimientos.append(chain.invoke({"noticia": noticia}))
  newsFeelings = pd.DataFrame({
      "Noticia": noticia,
      "sentimientos": sentimientos
  })
  newsFeelings.head()

  # transformamos la lista de cadenas que extraemos del dataframe anterior, en una lista comun, para su posterior analisis
  lista_sentimientos  = [elemento.strip() for cadena in sentimientos for elemento in cadena.split(',')]

  return lista_sentimientos
