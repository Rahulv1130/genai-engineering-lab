from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


from dotenv import load_dotenv

load_dotenv()

DB_DIR = "./chroma_db"
COLLECTION_NAME = "pdf_collection"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K_DOCS = 4

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the question using only the context below. "
            "If the question is generic like Hi, Hello and you think you can answer it the please do"
            "If you cant or If the answer is not in the context, say 'I don't know'.\n\n"
            "Context:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = PROMPT | llm | StrOutputParser()

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=DB_DIR,
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": TOP_K_DOCS},
)


while True:
    question = input("You: ").strip()

    if not question:
        continue
    if question.lower() in ("quit", "exit", "q"):
        print("Goodbye!")
        break

    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    answer = chain.invoke({"context": context, "question": question})

    print(f"\nBot: {answer}")
    print()