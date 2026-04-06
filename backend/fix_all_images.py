"""
Fix image URLs - use Open Library covers API (reliable)
Run: python fix_all_images.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, init_db
from app.models import Book

init_db()

# ISBN -> reliable cover URL mapping for all seeded books
ISBN_COVERS = {
    # seed_books.py
    "9780747532699": "https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg",
    "9780062315007": "https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg",
    "9780061935466": "https://covers.openlibrary.org/b/isbn/9780061935466-L.jpg",
    "9780743273565": "https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg",
    "9780735211292": "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg",
    "9781612680194": "https://covers.openlibrary.org/b/isbn/9781612680194-L.jpg",
    "9780451524935": "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg",
    "9780307887894": "https://covers.openlibrary.org/b/isbn/9780307887894-L.jpg",
    "9781585424337": "https://covers.openlibrary.org/b/isbn/9781585424337-L.jpg",
    "9780547928227": "https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg",
    "9781593279288": "https://covers.openlibrary.org/b/isbn/9781593279288-L.jpg",
    "9781577314806": "https://covers.openlibrary.org/b/isbn/9781577314806-L.jpg",
    "9788173711466": "https://covers.openlibrary.org/b/isbn/9788173711466-L.jpg",
    "9780307474278": "https://covers.openlibrary.org/b/isbn/9780307474278-L.jpg",
    "9780804139021": "https://covers.openlibrary.org/b/isbn/9780804139021-L.jpg",
    "9780141439518": "https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg",
    "9780062457714": "https://covers.openlibrary.org/b/isbn/9780062457714-L.jpg",
    "9780143130727": "https://covers.openlibrary.org/b/isbn/9780143130727-L.jpg",
    # seed_books2.py
    "9781594631931": "https://covers.openlibrary.org/b/isbn/9781594631931-L.jpg",
    "9780553380163": "https://covers.openlibrary.org/b/isbn/9780553380163-L.jpg",
    "9780062515926": "https://covers.openlibrary.org/b/isbn/9780062515926-L.jpg",
    "9780441013593": "https://covers.openlibrary.org/b/isbn/9780441013593-L.jpg",
    "9780553296983": "https://covers.openlibrary.org/b/isbn/9780553296983-L.jpg",
    "9780060850524": "https://covers.openlibrary.org/b/isbn/9780060850524-L.jpg",
    "9781982137274": "https://covers.openlibrary.org/b/isbn/9781982137274-L.jpg",
    "9780399590504": "https://covers.openlibrary.org/b/isbn/9780399590504-L.jpg",
    "9780439023481": "https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg",
    "9780374533557": "https://covers.openlibrary.org/b/isbn/9780374533557-L.jpg",
    "9780525478812": "https://covers.openlibrary.org/b/isbn/9780525478812-L.jpg",
    "9780451526342": "https://covers.openlibrary.org/b/isbn/9780451526342-L.jpg",
    "9781455586691": "https://covers.openlibrary.org/b/isbn/9781455586691-L.jpg",
    "9781582701707": "https://covers.openlibrary.org/b/isbn/9781582701707-L.jpg",
    "9781501135910": "https://covers.openlibrary.org/b/isbn/9781501135910-L.jpg",
    "9780316769174": "https://covers.openlibrary.org/b/isbn/9780316769174-L.jpg",
    "9780316017930": "https://covers.openlibrary.org/b/isbn/9780316017930-L.jpg",
    "9780525559474": "https://covers.openlibrary.org/b/isbn/9780525559474-L.jpg",
    "9780393316049": "https://covers.openlibrary.org/b/isbn/9780393316049-L.jpg",
    "9780345391803": "https://covers.openlibrary.org/b/isbn/9780345391803-L.jpg",
    "9780140449334": "https://covers.openlibrary.org/b/isbn/9780140449334-L.jpg",
    "9780307949486": "https://covers.openlibrary.org/b/isbn/9780307949486-L.jpg",
    "9780062316103": "https://covers.openlibrary.org/b/isbn/9780062316103-L.jpg",
    "9789380658742": "https://covers.openlibrary.org/b/isbn/9789380658742-L.jpg",
    # seed_books3.py
    "9780007276554": "https://covers.openlibrary.org/b/isbn/9780007276554-L.jpg",
    "9781524763138": "https://covers.openlibrary.org/b/isbn/9781524763138-L.jpg",
    "9780135957059": "https://covers.openlibrary.org/b/isbn/9780135957059-L.jpg",
    "9780132350884": "https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg",
    "9780316707046": "https://covers.openlibrary.org/b/isbn/9780316707046-L.jpg",
    "9780345539434": "https://covers.openlibrary.org/b/isbn/9780345539434-L.jpg",
    "9781599869773": "https://covers.openlibrary.org/b/isbn/9781599869773-L.jpg",
    "9780307588371": "https://covers.openlibrary.org/b/isbn/9780307588371-L.jpg",
    "9780544336261": "https://covers.openlibrary.org/b/isbn/9780544336261-L.jpg",
    "9780143419648": "https://covers.openlibrary.org/b/isbn/9780143419648-L.jpg",
    "9781416562603": "https://covers.openlibrary.org/b/isbn/9781416562603-L.jpg",
    "9788129104595": "https://covers.openlibrary.org/b/isbn/9788129104595-L.jpg",
    "9788129115300": "https://covers.openlibrary.org/b/isbn/9788129115300-L.jpg",
    "9780812979657": "https://covers.openlibrary.org/b/isbn/9780812979657-L.jpg",
    "9780143031031": "https://covers.openlibrary.org/b/isbn/9780143031031-L.jpg",
    "9780618485222": "https://covers.openlibrary.org/b/isbn/9780618485222-L.jpg",
    "9780395927205": "https://covers.openlibrary.org/b/isbn/9780395927205-L.jpg",
    "9780141321684": "https://covers.openlibrary.org/b/isbn/9780141321684-L.jpg",
    "9780553208849": "https://covers.openlibrary.org/b/isbn/9780553208849-L.jpg",
    "9780684801223": "https://covers.openlibrary.org/b/isbn/9780684801223-L.jpg",
    "9780140177398": "https://covers.openlibrary.org/b/isbn/9780140177398-L.jpg",
    "9780143039433": "https://covers.openlibrary.org/b/isbn/9780143039433-L.jpg",
    "9780140449136": "https://covers.openlibrary.org/b/isbn/9780140449136-L.jpg",
    "9780199232765": "https://covers.openlibrary.org/b/isbn/9780199232765-L.jpg",
    "9780374528379": "https://covers.openlibrary.org/b/isbn/9780374528379-L.jpg",
    "9780060934347": "https://covers.openlibrary.org/b/isbn/9780060934347-L.jpg",
    "9780141439471": "https://covers.openlibrary.org/b/isbn/9780141439471-L.jpg",
    "9780141439846": "https://covers.openlibrary.org/b/isbn/9780141439846-L.jpg",
    "9780141439570": "https://covers.openlibrary.org/b/isbn/9780141439570-L.jpg",
    "9780141439556": "https://covers.openlibrary.org/b/isbn/9780141439556-L.jpg",
    "9780141441146": "https://covers.openlibrary.org/b/isbn/9780141441146-L.jpg",
    "9780140449266": "https://covers.openlibrary.org/b/isbn/9780140449266-L.jpg",
    "9780451419439": "https://covers.openlibrary.org/b/isbn/9780451419439-L.jpg",
    "9780156012195": "https://covers.openlibrary.org/b/isbn/9780156012195-L.jpg",
    "9780679720201": "https://covers.openlibrary.org/b/isbn/9780679720201-L.jpg",
    "9780679723165": "https://covers.openlibrary.org/b/isbn/9780679723165-L.jpg",
    "9780060883287": "https://covers.openlibrary.org/b/isbn/9780060883287-L.jpg",
    "9780307389732": "https://covers.openlibrary.org/b/isbn/9780307389732-L.jpg",
    "9780385490818": "https://covers.openlibrary.org/b/isbn/9780385490818-L.jpg",
    "9780156030304": "https://covers.openlibrary.org/b/isbn/9780156030304-L.jpg",
    "9780812550702": "https://covers.openlibrary.org/b/isbn/9780812550702-L.jpg",
    "9780553293357": "https://covers.openlibrary.org/b/isbn/9780553293357-L.jpg",
    "9780441569595": "https://covers.openlibrary.org/b/isbn/9780441569595-L.jpg",
    "9780756404741": "https://covers.openlibrary.org/b/isbn/9780756404741-L.jpg",
    "9780553573404": "https://covers.openlibrary.org/b/isbn/9780553573404-L.jpg",
    "9780618346257": "https://covers.openlibrary.org/b/isbn/9780618346257-L.jpg",
    "9780064404990": "https://covers.openlibrary.org/b/isbn/9780064404990-L.jpg",
    "9780060853983": "https://covers.openlibrary.org/b/isbn/9780060853983-L.jpg",
    "9780345391810": "https://covers.openlibrary.org/b/isbn/9780345391810-L.jpg",
    "9781451648539": "https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg",
    "9781982181284": "https://covers.openlibrary.org/b/isbn/9781982181284-L.jpg",
    "9780316548182": "https://covers.openlibrary.org/b/isbn/9780316548182-L.jpg",
    "9781785044496": "https://covers.openlibrary.org/b/isbn/9781785044496-L.jpg",
    "9780062407801": "https://covers.openlibrary.org/b/isbn/9780062407801-L.jpg",
    "9780857197689": "https://covers.openlibrary.org/b/isbn/9780857197689-L.jpg",
    "9781250107817": "https://covers.openlibrary.org/b/isbn/9781250107817-L.jpg",
    "9780307352149": "https://covers.openlibrary.org/b/isbn/9780307352149-L.jpg",
}

db = SessionLocal()
try:
    updated = 0
    books = db.query(Book).all()
    for book in books:
        if book.isbn and book.isbn in ISBN_COVERS:
            new_url = ISBN_COVERS[book.isbn]
            if book.image_url != new_url:
                book.image_url = new_url
                updated += 1
                print(f"  [FIX] {book.title}")
    db.commit()
    print(f"\n[DONE] {updated} books image URLs updated!")
finally:
    db.close()
