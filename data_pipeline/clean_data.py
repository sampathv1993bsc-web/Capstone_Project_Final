from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "raw_books.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_books.csv"

# Load raw scraped data
if not RAW_FILE.exists():
    raise FileNotFoundError(f"Raw dataset not found: {RAW_FILE}. Run scrape_books.py first.")

df = pd.read_csv(RAW_FILE)
required = {"title", "price", "star_rating", "availability", "category"}
missing_columns = required - set(df.columns)
if missing_columns:
    raise ValueError(f"Raw dataset is missing required columns: {sorted(missing_columns)}")


def clean_price(value):
    try:
        cleaned_value = str(value).replace("Â£", "").replace("£", "").strip()
        return float(cleaned_value)
    except (ValueError, TypeError):
        return pd.NA


def clean_availability(value):
    normalized = str(value).strip().lower()
    if normalized.startswith("in stock"):
        return True
    if normalized.startswith("out of stock"):
        return False
    return pd.NA


# Clean numeric and categorical fields.
df["price_gbp"] = df["price"].apply(clean_price)
rating_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df["rating"] = df["star_rating"].map(rating_mapping)
df["in_stock"] = df["availability"].apply(clean_availability)

# Assignment-required handling of parse failures:
# numeric fields are median-imputed; rows with unrecoverable required
# categorical fields are dropped.
for column in ["price_gbp", "rating"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")
    if df[column].isna().any():
        median = df[column].median()
        if pd.isna(median):
            raise ValueError(f"Cannot median-impute {column}: no valid numeric values exist.")
        df[column] = df[column].fillna(median)

if df["in_stock"].isna().any():
    # Availability is boolean rather than numeric, so an unrecognized value
    # cannot be median-imputed. Drop only those affected rows and document it.
    df = df.dropna(subset=["in_stock"])

df = df.dropna(subset=["title", "category"]).copy()

df["rating"] = df["rating"].round().astype(int).clip(1, 5)
df["in_stock"] = df["in_stock"].astype(bool)

GBP_TO_INR = 105.50
df["price_inr"] = (df["price_gbp"].astype(float) * GBP_TO_INR).round(3)

cleaned_df = df[[
    "title", "price_gbp", "rating", "in_stock", "category", "price_inr"
]].copy()

cleaned_df["price_gbp"] = cleaned_df["price_gbp"].astype(float)
cleaned_df["rating"] = cleaned_df["rating"].astype(int)
cleaned_df["in_stock"] = cleaned_df["in_stock"].astype(bool)
cleaned_df["price_inr"] = cleaned_df["price_inr"].astype(float)

cleaned_df.to_csv(OUTPUT_FILE, index=False)

print("=" * 60)
print("FINAL CLEANED DATASET")
print("=" * 60)
print("Shape:", cleaned_df.shape)
print("Columns:", cleaned_df.columns.tolist())
print("Data types:\n", cleaned_df.dtypes)
print("Missing values:\n", cleaned_df.isna().sum())
print(f"GBP -> INR rate: 1 GBP = {GBP_TO_INR:.2f} INR")
print(f"Cleaned data saved to: {OUTPUT_FILE}")
