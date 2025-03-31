import os
import logging
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

logger = logging.getLogger(__name__)

PDF_PATH="/Users/sarit/Documents/appsmiths/ebooks/gaslift/[Hernandez,_Ali]_Fundamentals_of_gas_lift_engineer.pdf"

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=st.secrets["general"]["OPENAI_API_KEY"])

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Create a vector store using Chroma. Next time will read from disk.
persist_directory = "/Users/sarit/study/chat-and-llm-app/pdf_rag_chroma_vectorstore"
embedding = OpenAIEmbeddings(api_key=st.secrets["general"]["OPENAI_API_KEY"])
if os.path.isdir(persist_directory):
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    logger.info("Loading vectorstore from disk")
else:
    vectorstore = Chroma.from_documents(documents=splits, embedding=embedding, persist_directory=persist_directory)
    logger.info("Creating vectorstore and saving to disk")

retriever = vectorstore.as_retriever()

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

if __name__ == "__main__":
    # Example usage
    question = "What is the purpose of gas lift?"
    result = rag_chain.invoke({"input": question})
    print(result["answer"])
