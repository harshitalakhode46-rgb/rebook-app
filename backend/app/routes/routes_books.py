"""
Book Management Routes
"""
from typing import List, Optional
import json, os, shutil
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book, User
from app.schemas import BookBase, BookUpdate, BookResponse, BookWithSeller
from app.auth import get_current_user

router = APIRouter(prefix="/api/books")


@router.get("", response_model=List[BookResponse])
def list_books(
    skip: int = 0,
    limit: int = 200,
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Book).filter(Book.is_available == True)
    if category:
        query = query.filter(Book.category == category)
    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) |
            (Book.author.ilike(f"%{search}%"))
        )
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    if condition:
        query = query.filter(Book.condition == condition)
    return query.offset(skip).limit(limit).all()


@router.get("/seller/my-books", response_model=List[BookResponse])
def get_my_books(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Book).filter(Book.seller_id == current_user.id).all()


@router.get("/{book_id}", response_model=BookWithSeller)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: str = Form(...),
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = json.loads(book_data)
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    new_book = Book(**data, image_url=file_path, seller_id=current_user.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    # Award eco points to seller (+10 per listing)
    current_user.eco_points = (current_user.eco_points or 0) + 10
    db.commit()
    return new_book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.seller_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    for key, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.seller_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    db.delete(book)
    db.commit()
    return None
