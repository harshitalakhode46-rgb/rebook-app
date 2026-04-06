"""
Book Time Capsule + Reading Chain Routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BookMemory, ReadingChainEntry, Book
from app.schemas import BookMemoryCreate, BookMemoryResponse, ChainEntryCreate, ChainEntryResponse, MessageResponse
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/api/capsule")


# ── Time Capsule ──────────────────────────────────────────────────────────────

@router.post("/memory/{book_id}", response_model=BookMemoryResponse)
def add_memory(
    book_id: int,
    data: BookMemoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id, Book.seller_id == current_user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found or not yours")
    existing = db.query(BookMemory).filter(BookMemory.book_id == book_id).first()
    if existing:
        existing.memory = data.memory
        existing.year_read = data.year_read
        existing.mood_tag = data.mood_tag
        db.commit()
        db.refresh(existing)
        return existing
    mem = BookMemory(book_id=book_id, memory=data.memory, year_read=data.year_read, mood_tag=data.mood_tag)
    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem


@router.get("/memory/{book_id}", response_model=BookMemoryResponse)
def get_memory(book_id: int, db: Session = Depends(get_db)):
    mem = db.query(BookMemory).filter(BookMemory.book_id == book_id).first()
    if not mem:
        raise HTTPException(status_code=404, detail="No memory attached to this book")
    return mem


# ── Reading Chain ─────────────────────────────────────────────────────────────

@router.post("/chain/{book_id}", response_model=ChainEntryResponse)
def add_chain_entry(
    book_id: int,
    data: ChainEntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    already = db.query(ReadingChainEntry).filter(
        ReadingChainEntry.book_id == book_id,
        ReadingChainEntry.user_id == current_user.id
    ).first()
    if already:
        raise HTTPException(status_code=400, detail="You already added your entry to this book's chain")
    entry = ReadingChainEntry(book_id=book_id, user_id=current_user.id, note=data.note, city=data.city)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/chain/{book_id}", response_model=List[ChainEntryResponse])
def get_chain(book_id: int, db: Session = Depends(get_db)):
    return db.query(ReadingChainEntry).filter(ReadingChainEntry.book_id == book_id)\
        .order_by(ReadingChainEntry.read_at).all()
