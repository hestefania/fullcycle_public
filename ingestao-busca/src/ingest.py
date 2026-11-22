
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

from src.config import CONNECTION_STRING, COLLECTION_NAME
from src.embeddings import get_embeddings

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")


def ingest_pdf():
    """
    Executa a ingestão do PDF:
    1. Carrega o PDF.
    2. Divide em chunks de 1000 caracteres.
    3. Aplica overlap de 150 caracteres.
    4. Gera embeddings.
    5. Armazena no PostgreSQL com pgVector.
    """

    if not PDF_PATH:
        raise ValueError("PDF_PATH não configurado no arquivo .env")

    if not os.path.isfile(PDF_PATH):
        raise FileNotFoundError(
            f"Arquivo PDF não encontrado: {PDF_PATH}"
        )

    print("\nIniciando ingestão do PDF...\n")

    # 1. Carregar PDF
    loader = PyPDFLoader(PDF_PATH)

    documentos = loader.load()

    if not documentos:
        print("Nenhum conteúdo encontrado no PDF.")
        return

    print(f"PDF carregado: {PDF_PATH}")
    print(f"Total de páginas: {len(documentos)}")

    # 2. Dividir em chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )

    chunks = splitter.split_documents(documentos)

    if not chunks:
        print("Nenhum chunk foi gerado.")
        return

    print(f"Total de chunks gerados: {len(chunks)}")

    # 3. Gerar embeddings e armazenar no PostgreSQL
    embeddings = get_embeddings()

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True
    )

    vector_store.add_documents(chunks)

    print(f"Total de chunks armazenados: {len(chunks)}")

    print("\nIngestão concluída com sucesso!")


if __name__ == "__main__":
    ingest_pdf()
