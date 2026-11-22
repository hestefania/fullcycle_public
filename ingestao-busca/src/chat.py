
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector

from src.config import CONNECTION_STRING, COLLECTION_NAME
from src.embeddings import get_embeddings
from src.search import search_prompt

load_dotenv()

CHAT_MODEL = os.getenv("CHAT_MODEL")


def buscar_documentos(pergunta, vector_store, k=10):
    """
    Busca os 10 chunks mais relevantes no PostgreSQL.
    """

    return vector_store.similarity_search_with_score(
        query=pergunta,
        k=k
    )


def montar_contexto(resultados):
    """
    Monta o contexto com os documentos recuperados.
    """

    contexto = []

    for i, (documento, score) in enumerate(resultados):

        fonte = documento.metadata.get(
            "source", "Fonte desconhecida"
        )

        pagina = documento.metadata.get(
            "page", "N/A"
        )

        contexto.append(
            f"""
DOCUMENTO {i + 1}
Fonte: {fonte}
Página: {pagina}

Conteúdo:
{documento.page_content}
"""
        )

    return "\n\n".join(contexto)


def responder(pergunta, vector_store, llm, chain):
    """
    Executa o fluxo completo de consulta RAG.
    """

    print("\n[1/3] Buscando documentos...")

    resultados = buscar_documentos(
        pergunta,
        vector_store,
        k=10
    )

    if not resultados:
        return (
            "Não tenho informações necessárias para "
            "responder sua pergunta."
        )

    print(f"[2/3] {len(resultados)} documentos recuperados.")

    # Montar contexto
    contexto = montar_contexto(resultados)

    # Montar prompt utilizando search.py
    prompt = chain.invoke({
        "contexto": contexto,
        "pergunta": pergunta
    })

    print("[3/3] Consultando LLM...")

    # Consultar LLM
    resposta = llm.invoke(prompt)

    return resposta.content


def main():

    # Inicializar template do prompt
    chain = search_prompt()

    if not chain:
        print(
            "Não foi possível iniciar o chat. "
            "Verifique os erros de inicialização."
        )
        return

    if not CHAT_MODEL:
        print("CHAT_MODEL não configurado no arquivo .env.")
        return

    try:

        # Inicializar embeddings
        embeddings = get_embeddings()

        # Inicializar PostgreSQL + pgVector
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING,
            use_jsonb=True
        )

        # Inicializar LLM
        llm = ChatOpenAI(
            model=CHAT_MODEL,
            temperature=0
        )

    except Exception as erro:

        print(f"Erro ao inicializar o chat: {erro}")
        return

    print("=" * 60)
    print("       CHAT RAG - LANGCHAIN + POSTGRESQL")
    print("=" * 60)

    print("\nDigite 'sair' para encerrar.\n")

    while True:

        pergunta = input("Você: ").strip()

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("\nChat encerrado.")
            break

        if not pergunta:
            continue

        try:

            resposta = responder(
                pergunta,
                vector_store,
                llm,
                chain
            )

            print("\nAssistente:")
            print("-" * 60)
            print(resposta)
            print("-" * 60)

            print()

        except Exception as erro:

            print(f"\nErro ao processar pergunta: {erro}\n")


if __name__ == "__main__":
    main()
