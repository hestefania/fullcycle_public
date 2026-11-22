
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import (
    EMBEDDING_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
    GOOGLE_API_KEY,
    GOOGLE_EMBEDDING_MODEL
)


def get_embeddings():
    """
    Inicializa o modelo de embeddings conforme
    o provedor configurado no arquivo .env.
    """

    if EMBEDDING_PROVIDER == "openai":

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY não configurada no .env"
            )

        return OpenAIEmbeddings(
            model=OPENAI_EMBEDDING_MODEL,
            api_key=OPENAI_API_KEY
        )

    elif EMBEDDING_PROVIDER == "google":

        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY não configurada no .env"
            )

        return GoogleGenerativeAIEmbeddings(
            model=GOOGLE_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )

    else:
        raise ValueError(
            f"Provedor de embeddings inválido: {EMBEDDING_PROVIDER}"
        )
