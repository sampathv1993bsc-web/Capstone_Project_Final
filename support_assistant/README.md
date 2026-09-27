# Zepto Support Assistant

A local, offline-first RAG support assistant built from the eight supplied Zepto policy documents.

## Components

- `docs/` — 8 policy documents, one document per chunk.
- `ingest.py` — loads documents, embeds them with `all-MiniLM-L6-v2`, and stores them in ChromaDB.
- `graph.py` — LangGraph state, intent classification, retrieval, and answer generation.
- `prompt.py` — Role/Context/Task/Format/Length prompt with a negative constraint and few-shot example.
- `models.py` — Pydantic response schema.
- `main.py` — FastAPI `/ask` endpoint.
- `Dockerfile` — local container build.

## Architecture

```text
8 policy TXT files
       |
       v
ingest.py / one chunk per document
       |
       v
all-MiniLM-L6-v2 embeddings
       |
       v
ChromaDB: zepto_policies
       ^
       |
customer query -> classify_intent
                    |
          +---------+---------+
          |                   |
 policy_question        general_question
          |                   |
          v                   v
retrieve_and_answer     direct_answer
          |
          v
       top-3 chunks
          |
          v
Pydantic AnswerResponse
          |
          v
FastAPI POST /ask
```

## Mock baseline

`MOCK_LLM` defaults to `1`.

- `classify_intent`: deterministic keyword heuristic.
- `retrieve_and_answer`: always performs local embedding + ChromaDB retrieval, then returns `Based on the retrieved context: ...` from the top chunk.
- `direct_answer`: returns `I can only answer questions about Zepto policies right now.`
- No external LLM API call is needed.

## Run locally

From the repository root:

```bash
python -m support_assistant.ingest
uvicorn support_assistant.main:app --host 0.0.0.0 --port 7860
```

The ingestion step must report 8 documents and 8 stored chunks.

### Example call transcripts (default `MOCK_LLM=1`)

The following transcripts document the required deterministic mock-mode behavior. They are intended as the module submission examples; run the commands above after installing the dependencies and building the local ChromaDB index to reproduce them.

**Policy question**

Request:

```text
POST /ask
{"query":"What is the delivery fee below INR 149?"}
```

Response:

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard delivery is free on orders over INR 149; orders below this threshold incur a flat INR 25 delivery fee. Priority delivery, which reserves the next available rider slot, is available at checkout for an additional INR 15. Zepto does not currently deliver to addresses outside its listed serviceable pin codes.",
  "sources": ["doc_01", "doc_04", "doc_06"],
  "confidence": 1.0
}
```

**General question**

Request:

```text
POST /ask
{"query":"Tell me a joke"}
```

Response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

The policy response uses the top retrieved chunk and the general response bypasses retrieval, as required by the deterministic mock baseline.

## Optional real LLM

Set `MOCK_LLM=0` and provide `GROQ_API_KEY`. The real answer-generation path validates JSON against the Pydantic schema and retries up to two additional times after an invalid response. The optional real path is not required for the deterministic baseline.

## Docker

Build from the repository root:

```bash
docker build -t zepto-support-assistant -f support_assistant/Dockerfile .
docker run --rm -p 7860:7860 zepto-support-assistant
```

The Docker image installs the consolidated root requirements, copies the package, builds the ChromaDB index, and starts `support_assistant.main:app` on port 7860.
