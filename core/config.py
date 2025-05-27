import os
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = "doc/promtior.pdf"
DB_DIR = "models/faiss_index"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
