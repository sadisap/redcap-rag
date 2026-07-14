# REDCap RAG

A Retrieval-Augmented Generation (RAG) prototype built for an Applied AI research project at Vanderbilt University.

The project retrieves structured organizational data from REDCap, indexes it using both semantic and lexical retrieval techniques, and generates grounded answers using a locally hosted large language model.

## Architecture

```text
User Question
       │
       ▼
Hybrid Retrieval
├── Semantic Search (Sentence Transformers + Chroma)
└── Lexical Search (TF-IDF)
       │
Weighted Score Fusion
       │
Top Relevant REDCap Records
       │
Llama 3.2 (Ollama)
       │
Grounded Answer
```

## Features

- Retrieve records from REDCap using the REDCap API
- Authenticate securely using environment variables
- Build semantic document representations from REDCap records
- Generate embeddings using Sentence Transformers
- Store and query embeddings with Chroma
- Build a TF-IDF lexical index
- Perform hybrid retrieval using semantic and lexical search
- Combine retrieval scores using weighted score fusion
- Generate grounded answers with a locally hosted Llama 3.2 model through Ollama

## Project Structure

```text
src/
├── main.py
├── redcap_client.py
├── retrieval.py
├── keyword_retrieval.py
├── embedding_client.py
├── chroma_client.py
├── llm_client.py
└── utils.py
```

## Requirements

- Python 3.9+
- Ollama
- Llama 3.2 model

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the model:

```bash
ollama pull llama3.2:3b
```

## Run

```bash
python src/main.py
```

## Current Retrieval Pipeline

1. Retrieve records from REDCap.
2. Construct searchable document representations.
3. Build a Chroma vector index using Sentence Transformer embeddings.
4. Build a TF-IDF lexical index over the same documents.
5. Retrieve candidates using both semantic and lexical search.
6. Normalize and combine retrieval scores using weighted score fusion.
7. Pass the highest-ranked records to the LLM for answer generation.

## Future Work

- Richer semantic document construction
- Metadata-aware filtering
- Instrument-specific document templates
- Explainable retrieval with citations
- Retrieval evaluation and benchmarking
- Cross-instrument retrieval
- User interface for interactive querying