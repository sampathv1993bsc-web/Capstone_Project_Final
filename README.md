# Capstone Project — Data Pipeline, Analytics & Support Assistant

## Project Overview

This capstone project implements an end-to-end data engineering, analytics, machine learning, and AI support assistant workflow.

The project is divided into three main modules:

1. **Data Pipeline** — Web scraping, data cleaning, currency conversion, relational database loading, SQL analysis, and pandas verification.
2. **Analytics & Machine Learning** — Exploratory Data Analysis (EDA), preprocessing, classification, class-imbalance analysis, model tuning, regression, and model persistence using the Titanic dataset.
3. **Support Assistant** — A support assistant application using a knowledge base, retrieval, routing, and Docker-based deployment.

---

## Project Structure

```text
Capstone-project-main/
│
├── data_pipeline/
│   ├── scrape_books.py
│   ├── clean_data.py
│   ├── database.py
│   ├── run_queries.py
│   ├── pandas_verification.py
│   ├── queries.sql
│   ├── requirements.txt
│   └── README.md
│
├── analytics/
│   ├── eda.ipynb
│   ├── modeling.ipynb
│   ├── titanic.csv
│   ├── titanic_best_pipeline.joblib
│   └── README.md
│
├── support_assistant/
│   ├── Dockerfile
│   ├── graph.py
│   ├── ingest.py
│   ├── main.py
│   ├── models.py
│   ├── prompt.py
│   └── README.md
│
├── .gitignore
└── README.md
```

---

# Module 1 — Data Pipeline

The data pipeline module demonstrates an end-to-end data engineering workflow.

### Main steps

* Scrape product/book data from a public scraping-practice website
* Clean and transform the raw data
* Apply the required currency conversion
* Store the processed data in a relational SQLite database
* Execute SQL queries for analysis
* Verify the results using pandas

### Main files

* `scrape_books.py` — Scrapes the source data
* `clean_data.py` — Cleans and transforms the data
* `database.py` — Creates and loads the SQLite database
* `queries.sql` — SQL analysis queries
* `run_queries.py` — Executes SQL queries
* `pandas_verification.py` — Verifies SQL results using pandas

---

# Module 2 — Analytics & Machine Learning

This module implements an end-to-end analytics and predictive-modeling workflow using the Titanic dataset.

### Exploratory Data Analysis

The analysis includes:

* Dataset profiling
* Missing-value analysis
* Data cleaning
* Descriptive statistics
* Histograms and box plots
* Outlier analysis
* Survival-rate analysis
* Correlation analysis
* Multivariate visualizations
* Z-score standardization

### Machine Learning

The following classification models are implemented:

* Logistic Regression
* Decision Tree
* Random Forest

The workflow also includes:

* Stratified train-test splitting
* Numerical preprocessing
* Categorical preprocessing
* `ColumnTransformer`
* `Pipeline`
* Class-imbalance analysis
* SMOTE
* Random Forest hyperparameter tuning
* Cross-validation
* ROC-AUC evaluation
* Model persistence using Joblib

### Regression

A multivariate Linear Regression model is used to predict fare.

Evaluation metrics include:

* MAE
* RMSE
* R²
* Adjusted R²

### Main files

* `eda.ipynb` — Exploratory Data Analysis
* `modeling.ipynb` — Machine Learning and regression
* `titanic.csv` — Offline dataset
* `titanic_best_pipeline.joblib` — Saved ML pipeline

---

# Module 3 — Support Assistant

The support assistant module implements a knowledge-based support application.

It includes:

* Knowledge-base ingestion
* Retrieval
* Support-ticket handling
* Routing
* Prompt/model components
* Docker containerization

### Main files

* `ingest.py` — Knowledge-base ingestion
* `graph.py` — Application workflow/routing
* `models.py` — Model definitions
* `prompt.py` — Prompt configuration
* `main.py` — Application entry point
* `Dockerfile` — Container configuration

---

# Technologies Used

### Programming

* Python
* SQL

### Data & Machine Learning

* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Joblib
* imbalanced-learn / SMOTE

### Database

* SQLite

### AI / Application

* Retrieval-based support workflow
* Knowledge-base processing
* Docker

---

# How to Run

## Module 1

Navigate to the data pipeline directory:

```bash
cd data_pipeline
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline scripts in the required order.

---

## Module 2

Open the notebooks:

```text
analytics/eda.ipynb
analytics/modeling.ipynb
```

Run:

1. `eda.ipynb`
2. `modeling.ipynb`

The notebooks contain the complete analysis, visualizations, model training, evaluation, and results.

---

## Module 3

Navigate to:

```bash
cd support_assistant
```

Build the Docker image:

```bash
docker build -t support-assistant .
```

Run the container according to the configuration described in:

```text
support_assistant/README.md
```

---

# Reproducibility

The project includes committed datasets and saved artifacts where required so that the analysis can be reproduced without depending entirely on external data sources.

Random states and preprocessing pipelines are used where applicable to improve reproducibility.

---

# Project Outcome

This project demonstrates a complete workflow covering:

**Data Collection → Data Cleaning → Data Transformation → Database → SQL → Pandas → EDA → Machine Learning → Model Evaluation → Model Persistence → AI Support Assistant → Docker**

---

# Author

**Capstone Project**

Built as part of an AI / Data Science learning and project workflow.
