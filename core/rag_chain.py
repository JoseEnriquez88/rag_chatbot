import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_together import Together
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

load_dotenv()


PDF_PATH = "doc/promtior.pdf"
DB_DIR = "models/faiss_index"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def ensure_faiss_index():
    if os.path.exists(DB_DIR):
        return

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=300)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_DIR)

ensure_faiss_index()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)

retriever = db.as_retriever(search_kwargs={"k": 2})

llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.0,
    max_tokens=300,
    together_api_key=TOGETHER_API_KEY
)

system_prompt = """
Sos un asistente profesional sobre Promtior. Respondé solo con la información del documento.
Respondé a la pregunta de forma clara, completa y profesional, sin repetir la pregunta ni agregar encabezados innecesarios.
No incluyas frases como 'puede obtener más información', correos electrónicos ni referencias a sitios web.
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt.strip()),
    HumanMessagePromptTemplate.from_template("Contexto:\n{context}\n\nPregunta:\n{input}")
])

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


