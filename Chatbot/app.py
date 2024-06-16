from langchain_openai import ChatOpenAI
#importing chatOpenAi to manage interactions with OpenAI's language models
from langchain_core.prompts import ChatPromptTemplate
#Importing ChatPromptTemplate to structure and manage prompts with language models
from langchain_core.output_parsers import StrOutputParser
#import for the tast of text parsing at the output end

import streamlit as st #webapplication
import os
from dotenv import load_dotenv

load_dotenv()

#loading Environment variables
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2="true"

#Prompt Template

Prompt=ChatPromptTemplate.from_messages(
[
   ("system","You gonna answer everythink i ask about cricket"),
   ("user","Question:{question}")
]
)

#Streamlit Framework

st.title("Try out LLM model with Langchain and OpenAI")
input_text=st.text_input("write down your query")

#OpenAI LLM
LLM=ChatOpenAI(model="gpt-3.5-turbo") #model declaration
output_parser=StrOutputParser() #kind of parsing at the output end
chain=Prompt|LLM|output_parser #Chaining the actions inorder 

if input_text:
    st.write(chain.invoke({'question':input_text}))