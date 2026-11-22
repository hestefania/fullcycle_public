
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# POSTGRESQL
# ==========================================

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Validar configurações obrigatórias
postgres_config = {
    "POSTGRES_HOST": POSTGRES_HOST,
    "POSTGRES_PORT": POSTGRES_PORT,
    "POSTGRES_DB": POSTGRES_DB,
    "POSTGRES_USER": POSTGRES_USER,
    "POSTGRES_PASSWORD": POSTGRES_PASSWORD
}

for chave, valor in postgres_config.items():
    if not valor:
        raise ValueError(f"{chave} não configurado no arquivo .env")

# String de conexão
CONNECTION_STRING = (
    f"postgresql+psycopg://"
    f"{quote_plus(POSTGRES_USER)}:"
    f"{quote_plus(POSTGRES_PASSWORD)}@"
    f"{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

# ==========================================
# PGVECTOR
# ==========================================

COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

if not COLLECTION_NAME:
    raise ValueError("PG_VECTOR_COLLECTION_NAME não configurado no .env")

# ==========================================
# PDF
# ==========================================

PDF_PATH = os.getenv("PDF_PATH")

# ==========================================
# OPENAI
# ==========================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

# ==========================================
# GOOGLE GEMINI
# ==========================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

# ==========================================
# EMBEDDING PROVIDER
# ==========================================

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "").lower()

if EMBEDDING_PROVIDER not in ("openai", "google"):
    raise ValueError(
        "EMBEDDING_PROVIDER deve ser openai ou google no .env"
    )

# ==========================================
# CHAT
# ==========================================

CHAT_MODEL = os.getenv("CHAT_MODEL")

if not CHAT_MODEL:
    raise ValueError("CHAT_MODEL não configurado no .env")
