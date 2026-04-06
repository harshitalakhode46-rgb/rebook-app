"""
Seed script - adds sample books with real cover images
Run: python seed_books.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, init_db
from app.models import Book, User

init_db()

BOOKS = [
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "category": "Fiction",
        "isbn": "9780747532699",
        "condition": "Good",
        "price": 149.0,
        "description": "The first book in the magical Harry Potter series. A young boy discovers he's a wizard on his 11th birthday.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Fiction",
        "isbn": "9780062315007",
        "condition": "Like New",
        "price": 120.0,
        "description": "A philosophical novel about a young Andalusian shepherd who dreams of finding treasure.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg",
        "swap_available": False,
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "category": "Classic",
        "isbn": "9780061935466",
        "condition": "Good",
        "price": 99.0,
        "description": "A Pulitzer Prize-winning novel about racial injustice and moral growth in the American South.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780061935466-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category": "Classic",
        "isbn": "9780743273565",
        "condition": "Acceptable",
        "price": 79.0,
        "description": "A story of wealth, love, and the American Dream set in the Jazz Age.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg",
        "swap_available": False,
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "category": "Self-Help",
        "isbn": "9780735211292",
        "condition": "Like New",
        "price": 199.0,
        "description": "A practical guide to building good habits and breaking bad ones using tiny changes.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg",
        "swap_available": False,
    },
    {
        "title": "Rich Dad Poor Dad",
        "author": "Robert T. Kiyosaki",
        "category": "Finance",
        "isbn": "9781612680194",
        "condition": "Good",
        "price": 130.0,
        "description": "What the rich teach their kids about money that the poor and middle class do not.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781612680194-L.jpg",
        "swap_available": True,
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "category": "Classic",
        "isbn": "9780451524935",
        "condition": "Good",
        "price": 89.0,
        "description": "A dystopian novel about a totalitarian society where Big Brother watches everyone.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Lean Startup",
        "author": "Eric Ries",
        "category": "Business",
        "isbn": "9780307887894",
        "condition": "Like New",
        "price": 175.0,
        "description": "How today's entrepreneurs use continuous innovation to create successful businesses.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780307887894-L.jpg",
        "swap_available": False,
    },
    {
        "title": "Think and Grow Rich",
        "author": "Napoleon Hill",
        "category": "Self-Help",
        "isbn": "9781585424337",
        "condition": "Acceptable",
        "price": 85.0,
        "description": "A classic personal development book based on studying successful people.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781585424337-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "category": "Fantasy",
        "isbn": "9780547928227",
        "condition": "Good",
        "price": 140.0,
        "description": "Bilbo Baggins, a hobbit, goes on an unexpected adventure with a wizard and thirteen dwarves.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "category": "Technology",
        "isbn": "9781593279288",
        "condition": "Like New",
        "price": 250.0,
        "description": "A hands-on, project-based introduction to programming in Python.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781593279288-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Power of Now",
        "author": "Eckhart Tolle",
        "category": "Self-Help",
        "isbn": "9781577314806",
        "condition": "Good",
        "price": 110.0,
        "description": "A guide to spiritual enlightenment focusing on living in the present moment.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781577314806-L.jpg",
        "swap_available": False,
    },
    {
        "title": "Wings of Fire",
        "author": "A.P.J. Abdul Kalam",
        "category": "Biography",
        "isbn": "9788173711466",
        "condition": "Good",
        "price": 95.0,
        "description": "Autobiography of India's missile man and former President Dr. A.P.J. Abdul Kalam.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9788173711466-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Da Vinci Code",
        "author": "Dan Brown",
        "category": "Thriller",
        "isbn": "9780307474278",
        "condition": "Acceptable",
        "price": 105.0,
        "description": "A mystery thriller involving secret societies, religious history, and hidden codes.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780307474278-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Zero to One",
        "author": "Peter Thiel",
        "category": "Business",
        "isbn": "9780804139021",
        "condition": "Like New",
        "price": 180.0,
        "description": "Notes on startups and how to build the future by PayPal co-founder Peter Thiel.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780804139021-L.jpg",
        "swap_available": False,
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "category": "Classic",
        "isbn": "9780141439518",
        "condition": "Good",
        "price": 75.0,
        "description": "A romantic novel about the Bennet family and the proud Mr. Darcy in 19th century England.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Subtle Art of Not Giving a F*ck",
        "author": "Mark Manson",
        "category": "Self-Help",
        "isbn": "9780062457714",
        "condition": "Like New",
        "price": 155.0,
        "description": "A counterintuitive approach to living a good life by focusing on what truly matters.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780062457714-L.jpg",
        "swap_available": False,
    },
    {
        "title": "Ikigai",
        "author": "Héctor García & Francesc Miralles",
        "category": "Self-Help",
        "isbn": "9780143130727",
        "condition": "Like New",
        "price": 125.0,
        "description": "The Japanese secret to a long and happy life — finding your reason for being.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780143130727-L.jpg",
        "swap_available": True,
    },
]

db = SessionLocal()
try:
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("[ERROR] Admin user not found. Start the server once first, then run this script.")
        sys.exit(1)

    added = 0
    for b in BOOKS:
        exists = db.query(Book).filter(Book.isbn == b["isbn"]).first()
        if not exists:
            db.add(Book(**b, seller_id=admin.id, is_available=True))
            added += 1
            print(f"  [+] {b['title']}")
        else:
            print(f"  [SKIP] {b['title']} (already exists)")

    db.commit()
    print(f"\n[DONE] {added} books added successfully!")
finally:
    db.close()
