import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

#loading the groqapi key
Groq_api_key=os.environ['GROQ_API_KEY']


if "vector" not in st.session_state:
    st.session_state.embeddings=OllamaEmbeddings() #Assigning Embedding technique
    st.session_state.loader=WebBaseLoader("https://docs.smith.langchain.com") #defining websource
    st.session_state.document=st.session_state.loader.load() #loading the content
    st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=5)#splitting the content/text information into chunks
    st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.document[:50])
    st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

st.title("chatbot with groq")
llm=ChatGroq(groq_api_key=Groq_api_key,model_name="Gemma-7b-It")

prompt=ChatPromptTemplate.from_template("""Answer the question only on the basis of context provided only.
                                        please provide the most accurate response based on the question.
                                        <context>
                                        {context}
                                        <context>
                                        Questions:{input}
                                        """
                                        )


document_chain=create_stuff_documents_chain(llm,prompt)
retrieval=st.session_state.vectors.as_retriever()
retrieval_chain=create_retrieval_chain(retrieval,document_chain)

prompt=st.text_input("enter the prompt")

if prompt:
    response=retrieval_chain.invoke({'input':prompt})
    st.write(response['answer'])

    with st. expander ("Document Similarity Search"):
    # Find the relevant chunks
        for i,doc in enumerate (response["context" ]) :
            st.write(doc.page_content)
            st.write("-------")
