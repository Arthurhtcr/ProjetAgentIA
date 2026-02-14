from langchain_community.document_loaders import DirectoryLoader,UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_path = os.path.join(current_dir, "documents_projet")
persist_dir = os.path.join(current_dir, "chroma_db")

md_loader =  DirectoryLoader(
    path=docs_path,
    glob="**/*.txt",
    loader_cls=UnstructuredMarkdownLoader,
    show_progress=True)
md_docs = md_loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

chunks = text_splitter.split_documents(md_docs)



embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v3", model_kwargs={"trust_remote_code": True})
vectorstore = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory=persist_dir)