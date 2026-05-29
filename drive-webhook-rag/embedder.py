import logging
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import CHROMA_DIR, EMBEDDING_MODEL
load_dotenv()
logger = logging.getLogger(__name__)

# Use a local HuggingFace embedding model — no API key needed.
# Swap for OpenAIEmbeddings() or another provider if preferred.
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
    ".csv": CSVLoader,
}


def _get_loader(file_path: str):
    ext = Path(file_path).suffix.lower()
    loader_cls = LOADER_MAP.get(ext)
    if not loader_cls:
        raise ValueError(f"No loader available for extension: {ext}")
    return loader_cls(file_path)


def embed_and_store(local_path: str, file_meta: dict):
    """
    Load a file, split into chunks, embed, and persist in ChromaDB.
    Metadata (Drive file ID, name) is attached to every chunk.
    """
    logger.info(f"Loading document: {local_path}")
    loader = _get_loader(local_path)
    documents = loader.load()

    if not documents:
        logger.warning(f"No content extracted from {local_path}")
        return

    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(chunks)} chunks")

    # Attach Drive metadata to each chunk
    for chunk in chunks:
        chunk.metadata.update({
            "drive_file_id": file_meta.get("id"),
            "drive_file_name": file_meta.get("name"),
            "source": local_path,
        })

    vectorstore = Chroma(
        collection_name="drive_documents",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    vectorstore.add_documents(chunks)
    logger.info(f"Stored {len(chunks)} chunks in ChromaDB for: {file_meta.get('name')}")