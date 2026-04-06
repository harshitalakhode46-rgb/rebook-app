"""
Fix broken Amazon image URLs - replace with Open Library covers
Run from backend/ folder: python fix_images.py
"""
import os
import urllib.request
from app.database import SessionLocal, init_db
from app.models import Book

init_db()
db = SessionLocal()
os.makedirs("uploads", exist_ok=True)

# book_id -> (isbn, fallback_title_search)
ISBN_MAP = {
    1:  "9780735211292",  # Atomic Habits
    2:  "9780593086452",  # Psychology of Money
    3:  "9781593275846",  # Eloquent JavaScript
    4:  "9781524763138",  # Becoming
    5:  "9780143031031",  # Discovery of India
    6:  "9781593279288",  # Python Crash Course
    7:  "9780743273565",  # The Great Gatsby
    8:  "9781612680194",  # Rich Dad Poor Dad
    9:  "9780262033848",  # Introduction to Algorithms
    10: "9780006550686",  # God of Small Things
    11: "9780393609394",  # Astrophysics for People in a Hurry
    12: "9781501163913",  # Elon Musk
    13: "9780393317558",  # Guns Germs and Steel
    14: "9780321965516",  # Don't Make Me Think
    15: "9780198788607",  # The Selfish Gene
    16: "9780198788607",
    17: "9788129135728",  # The Race of My Life
    18: "9780198788607",
    19: "9780735211292",  # Atomic Habits duplicate
}

books = db.query(Book).all()
updated = 0

for book in books:
    isbn = ISBN_MAP.get(book.id)
    if not isbn:
        continue  # already has local uploads/ path, skip

    img_path = f"uploads/{isbn}.jpg"

    # Download if not already on disk
    if not os.path.exists(img_path):
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        try:
            urllib.request.urlretrieve(url, img_path)
            print(f"[IMG] {book.title}")
        except Exception as e:
            print(f"[WARN] Failed for '{book.title}': {e}")
            continue
    else:
        print(f"[CACHED] {book.title}")

    book.image_url = img_path
    updated += 1

db.commit()
print(f"\n[DONE] {updated} books updated.")
db.close()
