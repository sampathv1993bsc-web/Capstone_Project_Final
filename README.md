# Zepto Data & AI Platform — Capstone Project

This repository contains the three required capstone modules in **one repository**:

1. `data_pipeline/` — scrape → clean → currency conversion → SQLite → SQL → pandas verification.
2. `analytics/` — Titanic profiling → EDA → preprocessing → classification → imbalance analysis → tuning → regression → saved pipeline.
3. `support_assistant/` — policy ingestion → local embeddings → ChromaDB retrieval → LangGraph routing → Pydantic response → FastAPI → Docker.

The repository uses **one consolidated `requirements.txt` at the root**. Module-specific requirements are not duplicated.

## Project structure

```text
Capstone-project-main/
├── README.md
├── requirements.txt
├── .gitignore
├── data_pipeline/
│   ├── scrape_books.py
│   ├── clean_data.py
│   ├── database.py
│   ├── run_queries.py
│   ├── pandas_verification.py
│   ├── queries.sql
│   ├── README.md
│   ├── requirements.txt
│   ├── raw_books.csv
│   ├── cleaned_books.csv
│   ├── zepto_books.db
│   ├── query_outputs.txt
│   └── pandas_verification.txt
├── analytics/
│   ├── eda.ipynb
│   ├── modeling.ipynb
│   ├── titanic.csv
│   ├── titanic_best_pipeline.joblib
│   └── README.md
└── support_assistant/
    ├── __init__.py
    ├── docs/
    ├── ingest.py
    ├── prompt.py
    ├── graph.py
    ├── models.py
    ├── main.py
    ├── Dockerfile
    └── README.md
```

## 1. Installation

From the **repository root**:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

No paid API is required for the graded baseline.

## 2. Data Pipeline

The source is `books.toscrape.com`. The required fixed conversion is:

**1 GBP = 105.50 INR**

The database contains a normalized `categories` table and `books` table connected through a foreign key.

### Run from the repository root

```bash
python data_pipeline/scrape_books.py
python data_pipeline/clean_data.py
python data_pipeline/database.py
python data_pipeline/run_queries.py
python data_pipeline/pandas_verification.py
```

### Or run from inside `data_pipeline`

The scripts resolve their paths from their own location, so this also works:

```bash
cd data_pipeline
python scrape_books.py
python clean_data.py
python database.py
python run_queries.py
python pandas_verification.py
```

The scraper must produce at least 60 books across at least 3 categories. The saved SQL output demonstrates `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `BETWEEN`, `IN`, and `JOIN`.

## 3. Analytics

Run the notebooks in this order:

1. `analytics/eda.ipynb`
2. `analytics/modeling.ipynb`

The EDA notebook performs the single `sns.load_dataset("titanic")` load and immediately saves `analytics/titanic.csv`. The modeling notebook reads that committed CSV rather than independently loading Titanic again.

The modeling notebook uses a stratified split, training-only preprocessing, Logistic Regression, Decision Tree, Random Forest, baseline/class-weight/SMOTE comparison, Random Forest GridSearchCV with OOB scoring, fare regression, a combined model-comparison table, and a complete saved pipeline.

## 4. Support Assistant

The required baseline is deterministic mock mode. `MOCK_LLM` defaults to `1`.

First build the local ChromaDB index from the repository root:

```bash
python -m support_assistant.ingest
```

Then start FastAPI:

```bash
uvicorn support_assistant.main:app --host 0.0.0.0 --port 7860
```

Test a policy question:

```bash
curl -X POST http://127.0.0.1:7860/ask -H "Content-Type: application/json" -d "{\"query\":\"What is the delivery fee below INR 149?\"}"
```

Test a general question:

```bash
curl -X POST http://127.0.0.1:7860/ask -H "Content-Type: application/json" -d "{\"query\":\"Tell me a joke\"}"
```

Policy questions are classified using the required keyword heuristic, retrieve the top 3 ChromaDB chunks, and return a deterministic answer. General questions return the fixed mock response without retrieval.

## 5. Docker

Build from the **repository root**:

```bash
docker build -t zepto-support-assistant -f support_assistant/Dockerfile .
```

Run:

```bash
docker run --rm -p 7860:7860 zepto-support-assistant
```

The image builds the ChromaDB index during the image build and starts FastAPI on port 7860.

## 6. Git workflow

The supplied capstone requires at least one feature branch with at least two commits and a merge back into `main`. A reproducible example is:

```bash
git checkout -b feature/zepto-platform
git add .
git commit -m "feat: complete data pipeline"
git add .
git commit -m "feat: complete analytics and support assistant"
git checkout main
git merge --no-ff feature/zepto-platform -m "merge: complete capstone platform"
git log --graph --oneline --all
```

## Reproducibility and integrity

The committed CSV, SQLite database, notebooks, and joblib artifact are useful offline fallbacks, but the scripts/notebooks remain the source of reproducible computation. Do not invent or manually alter outputs to make metrics look better. Review and understand the implementation before submission.
