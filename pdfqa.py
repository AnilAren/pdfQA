import streamlit as st 
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAI
import os
from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
import json  # for reading and writing JSON files
load_dotenv()

# Define the file path for storing the history
history_file = "qa_history.json"

# Function to load the history from the file
def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return {}

# Function to save the history to the file
def save_history(history):
    with open(history_file, 'w') as f:
        json.dump(history, f)

def main():
    # Sidebar code should be inside the main function
    with st.sidebar:
        st.title("LLM PDF QA")
        selected_option = st.selectbox("Choose the Model", ["gpt-35-turbo", "text-davinci-002", "text-davinci-003"], index=0)

    # Load history
    qa_history = load_history()
    if not isinstance(qa_history, dict):  # Ensure qa_history is a dictionary
        qa_history = {}

    st.title("PDF QA")
    st.header("Chat with PDF ")
    
    # Upload pdf
    pdf = st.file_uploader("Upload your PDF", type='pdf')
    if pdf:
        pdf_name = pdf.name
        pdf_key = pdf_name  # Use PDF filename as the key
        if pdf_name not in qa_history:
            qa_history[pdf_key] = []  # Initialize an empty list for the PDF if not present
        
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        chunks = text_splitter.split_text(text=text)
        vector_store_file = "embeddings/" + pdf_name[:-4]  # removing .pdf extension
        
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-ada-002",
            openai_api_version="2023-05-15",
        )
        
        if os.path.exists(vector_store_file):
            vector_store = FAISS.load_local(vector_store_file, embeddings=embeddings, allow_dangerous_deserialization=True)
            st.write("Embeddings Loaded from Memory")
        else:
            vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            vector_store.save_local(vector_store_file)
            st.write("Embeddings Computation completed and saved")
        
        # Accept user question
        query = st.text_input("Ask questions about your pdf")
        if query:
            docs = vector_store.similarity_search(query=query, k=3)
            llm = AzureOpenAI(
                temperature=0.2,
                deployment_name=selected_option,
                model_name=selected_option,
                max_tokens=512
            )
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                qa_history[pdf_key].append((query, response))  # Store the question and answer for this PDF
                save_history(qa_history)  # Save the updated history
            st.info(response)
    
        # Display QA history for the selected PDF
        st.header("Question-Answer History for " + pdf_name)
        if pdf_key in qa_history:
            for q, a in qa_history[pdf_key]:
                st.subheader(f"Q: {q}")
                st.text_area(f"Answer:", value=a, height=100)
                st.write("---")
        else:
            st.write("No history available for this PDF.")

if __name__ == '__main__':
    main()
