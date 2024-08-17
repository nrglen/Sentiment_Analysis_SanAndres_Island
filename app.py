
from operator import itemgetter
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import pandas as pd

from DataPreparation import contents

prompt = ChatPromptTemplate.from_messages([
  ("system", "You are a sentiment analyzer for news articles.\n"
  "Read the following news article and determine 3 most important emotions,dont explain the emotion, only put the word for them, dont put a period after the last emotion"),

  ("human", "Analyze the following news article:\n\"{noticia}\"")])
#"Read the following news article and describe the emotions and sentiments you identify in the text."),
#("system","Read the following news article and determine if the new is positive, negativo or neutral for the tourism, dont explain why, only select the word that apply."),
model = "phi3:14b-medium-4k-instruct-q6_K"
# model = "gemma2:9b-instruct-q8_0"
llm = ChatOllama(temperature=0, model=model)

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

st.title("Hello")
st.bar_chart(newsFeelings)