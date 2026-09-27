from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "zepto_books.db"
QUERY_FILE = BASE_DIR / "queries.sql"
OUTPUT_FILE = BASE_DIR / "query_outputs.txt"

query_text = QUERY_FILE.read_text(encoding="utf-8")
queries = []
for statement in query_text.split(";"):
    lines = [line for line in statement.splitlines() if not line.strip().startswith("--")]
    sql = "\n".join(lines).strip()
    if sql:
        queries.append(sql)

if len(queries) < 5:
    raise ValueError(f"Expected at least 5 SQL queries; found {len(queries)}.")

outputs = ["=" * 70, "ZEPTO DATA & AI PLATFORM - MODULE 1", "SQL QUERY RESULTS", "=" * 70]
with sqlite3.connect(DATABASE_PATH) as connection:
    cursor = connection.cursor()
    for number, query in enumerate(queries, 1):
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        print(f"\n{'=' * 70}\nQUERY {number}\n{'=' * 70}\n{query}\n")
        print("Columns:", columns)
        for row in rows:
            print(row)
        outputs.extend([
            "=" * 70, f"QUERY {number}", "=" * 70,
            "SQL:", query, "", "Columns:", str(columns), "", "Results:",
            *(str(row) for row in rows), "", f"Number of rows: {len(rows)}", ""
        ])

OUTPUT_FILE.write_text("\n".join(outputs), encoding="utf-8")
print(f"Executed {len(queries)} queries. Output: {OUTPUT_FILE}")
