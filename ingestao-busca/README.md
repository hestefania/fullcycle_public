
# Ingestão e Busca Semântica com LangChain, PostgreSQL e pgVector

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![pgVector](https://img.shields.io/badge/pgVector-Vector%20Database-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-Embeddings%20%7C%20LLM-black)

## Sobre o projeto

Este projeto implementa uma solução de **RAG (Retrieval-Augmented Generation)** utilizando Python, LangChain, PostgreSQL e pgVector.

O objetivo é permitir a ingestão de documentos PDF, transformar seu conteúdo em vetores (embeddings), armazená-los em um banco de dados vetorial e disponibilizar uma interface de conversação via terminal.

As respostas são geradas por um modelo de linguagem (LLM), utilizando como contexto os documentos recuperados por similaridade semântica.

O sistema foi desenvolvido como parte do desafio de Ingestão e Busca Semântica da Full Cycle.

## Arquitetura da solução

O projeto está organizado em duas etapas principais:

### 1. Ingestão de documentos

- Leitura de arquivos PDF.
- Extração do conteúdo textual.
- Divisão do documento em chunks.
- Geração de embeddings.
- Armazenamento dos vetores no PostgreSQL utilizando pgVector.

### 2. Busca semântica e Chat RAG

- Recebimento de perguntas via terminal.
- Conversão da pergunta em embedding.
- Recuperação dos 10 documentos mais relevantes.
- Construção do contexto para o modelo de linguagem.
- Envio do contexto e da pergunta para a LLM.
- Retorno da resposta ao usuário.

O sistema utiliza instruções para restringir as respostas ao conteúdo recuperado dos documentos.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal |
| LangChain | Orquestração do RAG |
| OpenAI | Modelo de linguagem e embeddings |
| Google Gemini | Alternativa para geração de embeddings |
| PostgreSQL 17 | Banco de dados |
| pgVector | Armazenamento e busca vetorial |
| Docker | Containerização do banco |
| Docker Compose | Orquestração dos containers |
| PyPDF | Extração de conteúdo PDF |







## Estrutura do projeto

```text
ingestao-busca/
│
├── docker-compose.yml
├── requirements.txt
├── .env
├── .env.example
├── docs/
│   └── document.pdf
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── embeddings.py
    ├── ingest.py
    ├── search.py
    └── chat.py
```

## Descrição dos arquivos

- **`docker-compose.yml`**: configuração do PostgreSQL 17 com pgVector.
- **`requirements.txt`**: dependências Python.
- **`.env`**: configurações e credenciais do projeto.
- **`.env.example`**: modelo das variáveis de ambiente.
- **`docs/document.pdf`**: documento utilizado na ingestão.
- **`src/config.py`**: configurações de conexão com PostgreSQL.
- **`src/embeddings.py`**: configuração dos provedores de embeddings.
- **`src/ingest.py`**: processamento e armazenamento dos documentos.
- **`src/search.py`**: construção do prompt de consulta.
- **`src/chat.py`**: interface de conversação via terminal.
 

### Pré-requisitos
Antes de executar o projeto, é necessário possuir:

Python 3.10 ou superior.

Docker Desktop.

Docker Compose.

Chave de API da OpenAI.

Acesso à internet para utilização dos serviços de IA.


## Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/hestefania/fullcycle_public.git
```
 Acesse a pasta do projeto:


```bash
cd fullcycle_public/ingestao-busca
```

### 2. Criar o ambiente virtual
Windows (PowerShell):


``` powershell
python -m venv venv
```
Ativar:


```powershell
.\venv\Scripts\Activate.ps1
```

Caso exista bloqueio de execução de scripts:


```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
Com o ambiente virtual ativado:


```bash
python -m pip install --upgrade pip
```

Instalar as bibliotecas:

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente
Crie um arquivo .env na raiz do projeto.

Utilize o seguinte modelo:



```env

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Documentos
PDF_PATH=./docs/document.pdf

# Embeddings
EMBEDDING_PROVIDER=openai
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
GOOGLE_EMBEDDING_MODEL=models/embedding-001

# PostgreSQL Vector
PG_VECTOR_COLLECTION_NAME=documentos_pdf

# API Keys
OPENAI_API_KEY=sua_chave_openai
GOOGLE_API_KEY=sua_chave_google

# Modelo de linguagem
CHAT_MODEL=gpt-4.1-mini
Importante: substitua as chaves pelas suas credenciais válidas. Nunca publique o arquivo .env com credenciais reais no GitHub.
```




##  Executando o projeto
A execução deve seguir a ordem abaixo.

### 1. Iniciar o PostgreSQL com Docker
Execute na raiz do projeto:

```bash
docker compose up -d
```

O Docker Compose iniciará:

- PostgreSQL 17.
- Extensão pgVector.
- Volume persistente para os dados do banco.

Verifique os containers: 
```bash
docker compose ps
```

### 2. Executar a ingestão dos documentos
Com o banco de dados iniciado, execute:

```bash
python -m src.ingest
```
O processo realizará:

- Leitura do arquivo PDF
- Extração do conteúdo textual.
- Divisão do conteúdo em chunks.
- Geração dos embeddings.
-  Armazenamento dos vetores no PostgreSQL.

### 3. Executar o Chat RAG
Após concluir a ingestão, inicie o chat:

```bash
python -m src.chat
```
O sistema disponibilizará uma interface interativa no terminal.

Exemplo:
```
============================================================
       CHAT RAG - LANGCHAIN + POSTGRESQL
============================================================

Digite 'sair' para encerrar.

Você: Qual é o assunto principal do documento?

[1/3] Buscando documentos...
[2/3] 10 documentos recuperados.
[3/3] Consultando LLM...

Assistente:
------------------------------------------------------------
Resposta baseada no conteúdo do documento.
------------------------------------------------------------


```

Você:
Para encerrar:

```
sair

```


O processo de recuperação utiliza busca por similaridade vetorial.

Na implementação atual, são recuperados até 10 documentos (chunks) relevantes:


``` python
vector_store.similarity_search_with_score(
    query=pergunta,
    k=10
)
```


Os documentos recuperados são concatenados e utilizados como contexto para a construção do prompt.

O modelo de linguagem recebe o contexto e a pergunta do usuário.

**Regras de resposta**  
O modelo deve:
- Responder somente com base no contexto recuperado.
- Não inventar informações.
- Não utilizar conhecimento externo para complementar respostas.
- Informar quando não encontrar informações suficientes no documento.

Mensagem padrão:
- Não tenho informações necessárias para responder sua pergunta.

#### Configurações e personalização

É possível alterar algumas configurações por meio do arquivo `.env`:

| Variável | Descrição |
|---|---|
| `PDF_PATH` | Caminho do PDF |
| `EMBEDDING_PROVIDER` | Provedor dos embeddings |
| `OPENAI_EMBEDDING_MODEL` | Modelo de embeddings OpenAI |
| `GOOGLE_EMBEDDING_MODEL` | Modelo de embeddings Google |
| `PG_VECTOR_COLLECTION_NAME` | Nome da collection |
| `CHAT_MODEL` | Modelo de linguagem utilizado no chat |



Atenção: caso altere o modelo de embeddings, verifique a compatibilidade dimensional com os vetores já armazenados. Se a dimensão for diferente, será necessário recriar a collection e realizar uma nova ingestão.

 

## Ordem de execução

### 1. Subir o banco de dados:

```
docker compose up -d
```


### 2. Executar ingestão do PDF:


```
python -m  src.ingest
```

### 3. Rodar o chat:


```
python -m src.chat
```
Instalar dependências

```
pip install -r requirements.txt
```

### Considerações finais
Este projeto demonstra a aplicação prática de uma arquitetura RAG utilizando tecnologias modernas de inteligência artificial e bancos de dados vetoriais.

A solução permite transformar documentos não estruturados em uma base de conhecimento consultável por linguagem natural, utilizando recuperação semântica e modelos de linguagem.

Autor
Desenvolvido por Hestefania.

GitHub: https://github.com/hestefania 

Projeto desenvolvido para o desafio de Ingestão e Busca Semântica da Full Cycle.