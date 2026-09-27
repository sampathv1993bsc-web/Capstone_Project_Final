from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
RAW_OUTPUT = BASE_DIR / "raw_books.csv"

CATEGORIES = {
    "Travel": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "Mystery": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "Romance": "https://books.toscrape.com/catalogue/category/books/romance_8/index.html",
}


def scrape_category(category_name: str, start_url: str, session: requests.Session):
    books = []
    current_url = start_url
    page_number = 1

    while True:
        try:
            response = session.get(current_url, timeout=20)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(
                f"Could not access BooksToScrape while scraping {category_name} "
                f"page {page_number}: {exc}"
            ) from exc

        soup = BeautifulSoup(response.text, "html.parser")
        book_cards = soup.select("article.product_pod")
        if not book_cards:
            raise RuntimeError(
                f"No books found on {current_url}. The website structure may have changed."
            )

        print(f"Scraping {category_name} - Page {page_number} - {len(book_cards)} books")

        for book in book_cards:
            title_tag = book.select_one("h3 a")
            price_tag = book.select_one("p.price_color")
            rating_tag = book.select_one("p.star-rating")
            availability_tag = book.select_one("p.availability")
            if not all([title_tag, price_tag, rating_tag, availability_tag]):
                # A malformed card is skipped rather than crashing the complete scrape.
                continue

            classes = rating_tag.get("class", [])
            star_rating = classes[1] if len(classes) > 1 else "Unknown"
            books.append({
                "title": title_tag.get("title", title_tag.get_text(strip=True)),
                "price": price_tag.get_text(strip=True),
                "star_rating": star_rating,
                "availability": availability_tag.get_text(" ", strip=True),
                "category": category_name,
            })

        next_page = soup.select_one("li.next a")
        if next_page is None:
            break
        current_url = urljoin(current_url, next_page.get("href", ""))
        page_number += 1

    return books


def main():
    all_books = []
    with requests.Session() as session:
        session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; ZeptoCapstone/1.0)"})
        for category_name, start_url in CATEGORIES.items():
            all_books.extend(scrape_category(category_name, start_url, session))

    raw_df = pd.DataFrame(all_books).drop_duplicates(subset=["title", "category"])
    if len(raw_df) < 60 or raw_df["category"].nunique() < 3:
        raise RuntimeError(
            f"Acceptance criterion not met: {len(raw_df)} books across "
            f"{raw_df['category'].nunique()} categories."
        )

    raw_df.to_csv(RAW_OUTPUT, index=False)
    print(f"Scraping complete: {len(raw_df)} books across {raw_df['category'].nunique()} categories")
    print(f"Raw data saved to: {RAW_OUTPUT}")


if __name__ == "__main__":
    main()
