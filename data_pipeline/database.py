from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "zepto_books.db"
CLEANED_FILE = BASE_DIR / "cleaned_books.csv"

if not CLEANED_FILE.exists():
    raise FileNotFoundError(f"Cleaned dataset not found: {CLEANED_FILE}. Run clean_data.py first.")

cleaned_df = pd.read_csv(CLEANED_FILE)
required = {"title", "price_gbp", "price_inr", "rating", "in_stock", "category"}
missing = required - set(cleaned_df.columns)
if missing:
    raise ValueError(f"Cleaned dataset is missing required columns: {sorted(missing)}")

categories = sorted(cleaned_df["category"].dropna().astype(str).unique())
if len(categories) < 3:
    raise ValueError(f"Expected at least 3 categories; found {len(categories)}.")

with sqlite3.connect(DATABASE_PATH) as connection:
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("DROP TABLE IF EXISTS books;")
    cursor.execute("DROP TABLE IF EXISTS categories;")

    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT UNIQUE NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            price_gbp REAL NOT NULL,
            price_inr REAL NOT NULL,
            rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
            in_stock INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        );
    """)

    cursor.executemany(
        "INSERT INTO categories (category_name) VALUES (?);",
        [(category,) for category in categories]
    )

    category_lookup = dict(cursor.execute(
        "SELECT category_name, category_id FROM categories"
    ).fetchall())

    records = []
    for row in cleaned_df.itertuples(index=False):
        records.append((
            row.title,
            float(row.price_gbp),
            float(row.price_inr),
            int(row.rating),
            int(bool(row.in_stock)),
            category_lookup[str(row.category)],
        ))

    cursor.executemany("""
        INSERT INTO books
        (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?);
    """, records)

    table_names = [r[0] for r in cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()]
    book_count = cursor.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    invalid_fk = cursor.execute("""
        SELECT COUNT(*) FROM books
        WHERE category_id NOT IN (SELECT category_id FROM categories)
    """).fetchone()[0]
    books_per_category = cursor.execute("""
        SELECT c.category_name, COUNT(b.book_id)
        FROM categories c
        LEFT JOIN books b ON c.category_id = b.category_id
        GROUP BY c.category_id, c.category_name
        ORDER BY c.category_id
    """).fetchall()

print("=" * 60)
print("DATABASE CREATED AND LOADED")
print("=" * 60)
print("Database:", DATABASE_PATH)
print("Tables:", table_names)
print("Total books:", book_count)
print("Books by category:")
for category, count in books_per_category:
    print(f"  {category}: {count}")
print("Invalid foreign-key references:", invalid_fk)
