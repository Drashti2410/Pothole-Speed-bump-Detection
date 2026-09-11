import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()

def build_rag_chain():
    loader = DirectoryLoader("docs", glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="chroma_db")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
