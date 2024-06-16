import requests
import streamlit as st


#To retrive OpenAI model response
def get_openAI_response(input_text):
    response=requests.post("http://localhost:8000/essay/invoke",json={'input':{'topic':input_text}}) #to hit post at that specific url with a specified json inpt
    return response.json()['output']['content']#collecting the response

#To retrive Llama model response
def get_ollama_response(input_text):
    response=requests.post("http://localhost:8000/poem/invoke",json={'input':{'topic':input_text}})
    return response.json()['output']['content']

#Streamlit framework
st.title('Cricket chatbot with Llama and Gpt')
input_text=st.text_input('ask for eassay on cricket')
input_text1=st.text_input('ask for poem on cricket')


#Exceuting openAI
if input_text:
    st.write(get_openAI_response(input_text))

#Executing ollama 
if input_text1:
    st.write(get_ollama_response(input_text1))
