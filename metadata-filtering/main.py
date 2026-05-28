from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


documents = [
    Document(
        page_content="The new product launch is scheduled for Q3 2025 and focuses on AI-driven analytics.",
        metadata={
            "source": "report_2025.pdf",
            "department": "marketing",
            "year": 2025,
        },
    ),
    Document(
        page_content="Our Q1 2024 earnings were significantly boosted by the European market expansion.",
        metadata={
            "source": "financials_2024.pdf",
            "department": "finance",
            "year": 2024,
        },
    ),
    Document(
        page_content="Internal memo detailing the revised company social media policy for all departments.",
        metadata={
            "source": "policy_memo.txt",
            "department": "hr",
            "year": 2024,
        },
    ),
    Document(
        page_content="Quarterly report predicting strong growth in the Asian AI sector for 2025.",
        metadata={
            "source": "market_analysis.pdf",
            "department": "marketing",
            "year": 2025,
        },
    ),
]


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="test",
)


# Query without metadata filter
query = "What about our financials?"
results = vectorstore.similarity_search(query, k=2)

print("\n--- Standard Search (Top 2) ---")
for doc in results:
    print(f"Content: {doc.page_content[:50]}...")
    print(f"Metadata: {doc.metadata}")
    print("-" * 15)


# Query without metadata filter
finance_filter = {"department": "finance"}

query = "What about our financials?"
finance_results = vectorstore.similarity_search(
    query,
    k=2,
    filter=finance_filter
)

print("\n--- Filtered Search (Department = 'finance') ---")
for doc in finance_results:
    print(f"Content: {doc.page_content[:50]}...")
    print(f"Metadata: {doc.metadata}")
    print("-" * 15)