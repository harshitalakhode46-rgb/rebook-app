"""
Seed script - adds 25 new books (not already in DB)
Run: python seed_books2.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, init_db
from app.models import Book, User

init_db()

BOOKS = [
    {
        "title": "The Kite Runner",
        "author": "Khaled Hosseini",
        "category": "Fiction",
        "isbn": "9781594631931",
        "condition": "Good",
        "price": 115.0,
        "description": "A powerful story of friendship, betrayal, and redemption set in Afghanistan.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781594631931-L.jpg",
        "swap_available": True,
    },
    {
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "category": "Science",
        "isbn": "9780553380163",
        "condition": "Good",
        "price": 130.0,
        "description": "Stephen Hawking's landmark book on cosmology, black holes, and the nature of time.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780553380163-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Monk Who Sold His Ferrari",
        "author": "Robin Sharma",
        "category": "Self-Help",
        "isbn": "9780062515926",
        "condition": "Like New",
        "price": 120.0,
        "description": "A fable about fulfilling your dreams and reaching your destiny.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780062515926-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Sherlock Holmes: The Complete Novels",
        "author": "Arthur Conan Doyle",
        "category": "Mystery",
        "isbn": "9780743273566",
        "condition": "Acceptable",
        "price": 160.0,
        "description": "The complete collection of Sherlock Holmes detective stories.",
        "image_url": "https://covers.openlibrary.org/b/isbn//9780743273566-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "category": "Science Fiction",
        "isbn": "9780441013593",
        "condition": "Good",
        "price": 175.0,
        "description": "An epic science fiction saga set on the desert planet Arrakis.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780441013593-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Diary of a Young Girl",
        "author": "Anne Frank",
        "category": "Biography",
        "isbn": "9780553296983",
        "condition": "Good",
        "price": 90.0,
        "description": "The famous diary of Anne Frank written while hiding during the Nazi occupation.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780553296983-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "category": "Classic",
        "isbn": "9780060850524",
        "condition": "Acceptable",
        "price": 95.0,
        "description": "A dystopian novel set in a futuristic World State of genetically modified citizens.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780060850524-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The 7 Habits of Highly Effective People",
        "author": "Stephen R. Covey",
        "category": "Self-Help",
        "isbn": "9781982137274",
        "condition": "Like New",
        "price": 185.0,
        "description": "Powerful lessons in personal change and effectiveness.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781982137274-L.jpg",
        "swap_available": False,
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "category": "Biography",
        "isbn": "9780399590504",
        "condition": "Like New",
        "price": 145.0,
        "description": "A memoir about a woman who grows up in a survivalist family and educates herself.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780399590504-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "category": "Fiction",
        "isbn": "9780439023481",
        "condition": "Good",
        "price": 110.0,
        "description": "In a dystopian future, teenagers are forced to fight to the death in a televised event.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "category": "Psychology",
        "isbn": "9780374533557",
        "condition": "Good",
        "price": 195.0,
        "description": "Explores the two systems that drive the way we think — fast intuition and slow logic.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780374533557-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Fault in Our Stars",
        "author": "John Green",
        "category": "Romance",
        "isbn": "9780525478812",
        "condition": "Like New",
        "price": 100.0,
        "description": "A love story between two teenagers who meet at a cancer support group.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780525478812-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Animal Farm",
        "author": "George Orwell",
        "category": "Classic",
        "isbn": "9780451526342",
        "condition": "Acceptable",
        "price": 70.0,
        "description": "A satirical allegory of Soviet totalitarianism told through farm animals.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780451526342-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Deep Work",
        "author": "Cal Newport",
        "category": "Self-Help",
        "isbn": "9781455586691",
        "condition": "Like New",
        "price": 165.0,
        "description": "Rules for focused success in a distracted world.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781455586691-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Secret",
        "author": "Rhonda Byrne",
        "category": "Self-Help",
        "isbn": "9781582701707",
        "condition": "Good",
        "price": 105.0,
        "description": "Reveals the most powerful law in the universe — the law of attraction.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781582701707-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Shoe Dog",
        "author": "Phil Knight",
        "category": "Business",
        "isbn": "9781501135910",
        "condition": "Good",
        "price": 155.0,
        "description": "A memoir by the creator of Nike — the story of building one of the world's most iconic brands.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9781501135910-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "category": "Classic",
        "isbn": "9780316769174",
        "condition": "Acceptable",
        "price": 85.0,
        "description": "A story of teenage rebellion and alienation narrated by the iconic Holden Caulfield.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780316769174-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Outliers",
        "author": "Malcolm Gladwell",
        "category": "Psychology",
        "isbn": "9780316017930",
        "condition": "Good",
        "price": 140.0,
        "description": "The story of success — what makes high-achievers different.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780316017930-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "category": "Fiction",
        "isbn": "9780525559474",
        "condition": "Like New",
        "price": 135.0,
        "description": "Between life and death there is a library with books of every life you could have lived.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780525559474-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Surely You're Joking, Mr. Feynman!",
        "author": "Richard P. Feynman",
        "category": "Science",
        "isbn": "9780393316049",
        "condition": "Good",
        "price": 120.0,
        "description": "Adventures of a curious character — the Nobel Prize-winning physicist's memoirs.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780393316049-L.jpg",
        "swap_available": True,
    },
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "category": "Science Fiction",
        "isbn": "9780345391803",
        "condition": "Good",
        "price": 115.0,
        "description": "A comedic science fiction series following the misadventures of Arthur Dent.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780345391803-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Meditations",
        "author": "Marcus Aurelius",
        "category": "Philosophy",
        "isbn": "9780140449334",
        "condition": "Like New",
        "price": 95.0,
        "description": "Personal writings of the Roman Emperor — a timeless guide to Stoic philosophy.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780140449334-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "category": "Thriller",
        "isbn": "9780307949486",
        "condition": "Good",
        "price": 130.0,
        "description": "A gripping mystery thriller involving a journalist and a hacker investigating a decades-old disappearance.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780307949486-L.jpg",
        "swap_available": True,
    },
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "category": "History",
        "isbn": "9780062316103",
        "condition": "Like New",
        "price": 190.0,
        "description": "How Homo sapiens came to dominate the Earth — a sweeping history of humankind.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9780062316103-L.jpg",
        "swap_available": False,
    },
    {
        "title": "The Immortals of Meluha",
        "author": "Amish Tripathi",
        "category": "Mythology",
        "isbn": "9789380658742",
        "condition": "Good",
        "price": 100.0,
        "description": "The first book of the Shiva Trilogy — a fictional retelling of Lord Shiva as a mortal hero.",
        "image_url": "https://covers.openlibrary.org/b/isbn/9789380658742-L.jpg",
        "swap_available": True,
    },
]

db = SessionLocal()
try:
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("[ERROR] Admin user not found. Start the server once first.")
        sys.exit(1)

    # Get all existing ISBNs
    existing_isbns = {b.isbn for b in db.query(Book.isbn).all()}

    added = 0
    for b in BOOKS:
        if b["isbn"] in existing_isbns:
            print(f"  [SKIP] {b['title']}")
            continue
        db.add(Book(**b, seller_id=admin.id, is_available=True))
        added += 1
        print(f"  [+] {b['title']}")

    db.commit()
    print(f"\n[DONE] {added} new books added!")
finally:
    db.close()
