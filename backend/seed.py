"""
Seed script - adds sample users and books with cover images
Run from backend/ folder: python seed.py
"""
import os
import urllib.request
from app.database import SessionLocal, init_db
from app.models import User, Book
from app.auth import hash_password

init_db()
db = SessionLocal()

os.makedirs("uploads", exist_ok=True)

# ── Sample books: (title, author, category, condition, price, description, isbn, cover_url)
BOOKS = [
    (
        "The Alchemist",
        "Paulo Coelho",
        "Fiction",
        "like_new",
        149.0,
        "A magical story about a young shepherd's journey to find treasure and follow his dreams.",
        "9780062315007",
        "https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg",
    ),
    (
        "Atomic Habits",
        "James Clear",
        "Self-Help",
        "good",
        199.0,
        "Tiny changes, remarkable results. A proven framework for building good habits.",
        "9780735211292",
        "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg",
    ),
    (
        "Harry Potter and the Sorcerer's Stone",
        "J.K. Rowling",
        "Fiction",
        "acceptable",
        120.0,
        "The boy who lived. A young wizard discovers his magical heritage on his 11th birthday.",
        "9780439708180",
        "https://covers.openlibrary.org/b/isbn/9780439708180-L.jpg",
    ),
    (
        "Rich Dad Poor Dad",
        "Robert T. Kiyosaki",
        "Finance",
        "good",
        175.0,
        "What the rich teach their kids about money that the poor and middle class do not.",
        "9781612680194",
        "https://covers.openlibrary.org/b/isbn/9781612680194-L.jpg",
    ),
    (
        "To Kill a Mockingbird",
        "Harper Lee",
        "Fiction",
        "like_new",
        130.0,
        "A gripping tale of racial injustice and childhood innocence in the American South.",
        "9780061935466",
        "https://covers.openlibrary.org/b/isbn/9780061935466-L.jpg",
    ),
    (
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "Fiction",
        "good",
        99.0,
        "A story of wealth, love, and the American Dream set in the roaring 1920s.",
        "9780743273565",
        "https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg",
    ),
    (
        "Python Crash Course",
        "Eric Matthes",
        "Education",
        "like_new",
        299.0,
        "A hands-on, project-based introduction to programming in Python.",
        "9781593279288",
        "https://covers.openlibrary.org/b/isbn/9781593279288-L.jpg",
    ),
    (
        "The Lean Startup",
        "Eric Ries",
        "Business",
        "good",
        220.0,
        "How today's entrepreneurs use continuous innovation to create successful businesses.",
        "9780307887894",
        "https://covers.openlibrary.org/b/isbn/9780307887894-L.jpg",
    ),
    (
        "Sapiens",
        "Yuval Noah Harari",
        "Non-Fiction",
        "like_new",
        250.0,
        "A brief history of humankind from the Stone Age to the present.",
        "9780062316097",
        "https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg",
    ),
    (
        "1984",
        "George Orwell",
        "Fiction",
        "acceptable",
        89.0,
        "A dystopian novel about totalitarianism, surveillance, and the power of truth.",
        "9780451524935",
        "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg",
    ),
]

# ── Create seller user
seller = db.query(User).filter(User.username == "bookseller").first()
if not seller:
    seller = User(
        email="seller@rebook.com",
        username="bookseller",
        hashed_password=hash_password("seller123"),
        full_name="Book Seller",
        is_active=True,
    )
    db.add(seller)
    db.commit()
    db.refresh(seller)
    print("[OK] Seller user created: bookseller / seller123")
else:
    print("[INFO] Seller user already exists")

# ── Download covers and insert books
added = 0
for title, author, category, condition, price, description, isbn, cover_url in BOOKS:
    exists = db.query(Book).filter(Book.title == title).first()
    if exists:
        print(f"[SKIP] '{title}' already exists")
        continue

    # Download cover image
    img_filename = f"{isbn}.jpg"
    img_path = f"uploads/{img_filename}"
    if not os.path.exists(img_path):
        try:
            urllib.request.urlretrieve(cover_url, img_path)
            print(f"[IMG] Downloaded cover for '{title}'")
        except Exception as e:
            img_path = "uploads/download.jpg"  # fallback
            print(f"[WARN] Cover download failed for '{title}': {e}, using fallback")

    book = Book(
        title=title,
        author=author,
        category=category,
        condition=condition,
        price=price,
        description=description,
        isbn=isbn,
        image_url=img_path,
        is_available=True,
        seller_id=seller.id,
    )
    db.add(book)
    added += 1

db.commit()
print(f"\n[DONE] {added} books added.")
db.close()
