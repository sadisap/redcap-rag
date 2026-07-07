# REDCap RAG

A prototype Retrieval-Augmented Generation (RAG) workflow built for an Applied AI research project at Vanderbilt University.

## Current Functionality

* Connects to a REDCap project through the REDCap API
* Authenticates using an API token stored in a `.env` file
* Retrieves REDCap records as JSON
* Filters and cleans retrieved records
* Passes retrieved records to a local open-source LLM (Llama 3.2 via Ollama)
* Generates answers using only the retrieved REDCap data

## Project Structure

```text
src/
├── main.py
├── redcap_client.py
├── utils.py
└── llm_client.py
```

## Run

```bash
pip install -r requirements.txt
python3 src/main.py
```

## Next Steps

* Improve retrieval based on user queries
* Explore embedding-based retrieval and vector databases
* Expand into a more complete research assistant for REDCap data