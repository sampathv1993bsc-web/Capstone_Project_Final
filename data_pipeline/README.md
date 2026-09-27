# Module 1 — Data Pipeline

## Purpose

This module implements the required scrape → clean → convert → relational database → SQL → pandas workflow.

## Run

From the repository root:

```bash
python data_pipeline/scrape_books.py
python data_pipeline/clean_data.py
python data_pipeline/database.py
python data_pipeline/run_queries.py
python data_pipeline/pandas_verification.py
```

The same commands work from inside `data_pipeline` because the scripts resolve their paths from `__file__`.

## Data source

`books.toscrape.com` is used as the public scraping-practice source. The scraper collects the Travel, Mystery, and Romance categories and follows pagination until all books in those categories are collected. It verifies that the final raw dataset has at least 60 books across at least 3 categories.

## Cleaning decisions

- `price` is parsed to `price_gbp` as `float`.
- `star_rating` values One–Five are mapped to integer `rating` values 1–5.
- Availability beginning with `In stock` becomes `True`; availability beginning with `Out of stock` becomes `False`.
- Numeric parsing failures in `price_gbp` or `rating` are median-imputed.
- Unrecognized availability is not safely median-imputable because it is categorical; only rows with unrecognized availability are dropped.
- Rows missing the required title/category fields are dropped.
- `price_inr` is calculated with the required fixed rate **1 GBP = 105.50 INR**.

## Database

The SQLite schema contains:

```text
categories(category_id PRIMARY KEY, category_name UNIQUE)
books(book_id PRIMARY KEY, ..., category_id FOREIGN KEY -> categories.category_id)
```

Categories are derived from the cleaned dataset rather than hard-coded.

## SQL

`queries.sql` contains six queries covering:

- SELECT + WHERE
- ORDER BY + LIMIT
- DISTINCT
- BETWEEN
- IN
- JOIN

`run_queries.py` executes them and saves the SQL and outputs to `query_outputs.txt`.

## Pandas verification

`pandas_verification.py` uses `pd.read_sql()` for multiple queries and reproduces the required SQL JOIN using `pd.merge()`. The SQL and pandas results are compared after equivalent ordering/limiting and numeric normalization.
