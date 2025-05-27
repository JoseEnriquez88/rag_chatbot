from langchain_together import Together
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from .config import TOGETHER_API_KEY
from .embeddings import ensure_faiss_index, load_vectorstore
from .prompts import prompt

ensure_faiss_index()
db = load_vectorstore()
retriever = db.as_retriever(search_kwargs={"k": 2})

llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.0,
    max_tokens=300,
    together_api_key=TOGETHER_API_KEY,
)

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

def ask_question(query: str) -> str:
    original = query.strip()

    if "promtior" not in original.lower():
        query = f"{original.strip()} (refiriéndose a Promtior)"

    response = retrieval_chain.invoke({"input": query})["answer"]
    clean = response.strip()

    if clean.lower().startswith("respuesta:"):
        clean = clean[len("respuesta:"):].strip()

    for stop in ["Para obtener más información", "@promtior", "http", "www."]:
        if stop.lower() in clean.lower():
            clean = clean.split(stop)[0].strip()
    return clean
