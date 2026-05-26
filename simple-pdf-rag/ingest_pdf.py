from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


pdf_path = "./pdfRead.pdf"


# Load the Document
loader = PyPDFLoader(pdf_path)
documents = loader.load()


# Create chunks
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

print("PDF successfully stored in Vector DB")