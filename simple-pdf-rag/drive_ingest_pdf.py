import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

file_id = "1eyczaEIAVZm5KsaPY1mIWdBTEjFdqsmp"

download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

response = requests.get(download_url)

print("Document Downloaded Successfully ✅")

pdf_path = "./temp.pdf"

with open(pdf_path, "wb") as f:
    f.write(response.content)

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print("Document Loaded Successfully ✅")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
texts = text_splitter.split_documents(documents)

# Create embeddings and store in DB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="pdf_collection",
)

print("PDF successfully Downloaded and stored in Vector DB ✅")

# Delete the Temp File
if os.path.exists(pdf_path):
    os.remove(pdf_path)