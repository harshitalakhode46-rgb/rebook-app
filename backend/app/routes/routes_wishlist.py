"""
Wishlist Routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Wishlist, Book, User
from app.schemas import WishlistResponse, MessageResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/wishlist")


@router.get("", response_model=List[WishlistResponse])
def get_wishlist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()


@router.post("/{book_id}", response_model=MessageResponse)
def add_to_wishlist(book_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    existing = db.query(Wishlist).filter(Wishlist.user_id == current_user.id, Wishlist.book_id == book_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in wishlist")
    db.add(Wishlist(user_id=current_user.id, book_id=book_id))
    db.commit()
    return {"message": "Added to wishlist"}


@router.delete("/{book_id}", response_model=MessageResponse)
def remove_from_wishlist(book_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Wishlist).filter(Wishlist.user_id == current_user.id, Wishlist.book_id == book_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not in wishlist")
    db.delete(item)
    db.commit()
    return {"message": "Removed from wishlist"}
