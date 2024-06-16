from langchain.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langserve import add_routes #for multiple route assignments
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

#loading Environment variables
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

#fastapi instantiation
#fastapi object
app=FastAPI(
    title="Langchain server",
    version="1.0",
    description="API server"
)

add_routes(
    app,
    ChatOpenAI(),
    path='/openai'
)

model=ChatOpenAI() #first model from openai
llm=Ollama(model='llama2') #Second model

#Prompt Template
prompt1=ChatPromptTemplate.from_template("write me an essay about {topic} in 100 words") #the specific prompt for Chatopenai model
prompt2=ChatPromptTemplate.from_template("write me an poem about {topic} in 100 words") #this one for open source llm model

add_routes(
    app,
    prompt1|model,
    path='/essay'
)


add_routes(
    app,
    prompt2|llm,
    path='/poem'
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
