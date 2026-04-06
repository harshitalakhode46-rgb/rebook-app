"""
Book Swap Routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SwapOffer, Book, User
from app.schemas import SwapOfferCreate, SwapOfferResponse, MessageResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/swap")


@router.post("", response_model=SwapOfferResponse)
def create_swap_offer(
    data: SwapOfferCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    wanted = db.query(Book).filter(Book.id == data.wanted_book_id).first()
    if not wanted:
        raise HTTPException(status_code=404, detail="Wanted book not found")
    if not wanted.swap_available:
        raise HTTPException(status_code=400, detail="This book is not available for swap")
    if wanted.seller_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot swap with your own book")

    offered = db.query(Book).filter(Book.id == data.offered_book_id, Book.seller_id == current_user.id).first()
    if not offered:
        raise HTTPException(status_code=404, detail="Offered book not found or not yours")

    existing = db.query(SwapOffer).filter(
        SwapOffer.requester_id == current_user.id,
        SwapOffer.wanted_book_id == data.wanted_book_id,
        SwapOffer.status == "pending"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already have a pending swap offer for this book")

    offer = SwapOffer(
        requester_id=current_user.id,
        owner_id=wanted.seller_id,
        wanted_book_id=data.wanted_book_id,
        offered_book_id=data.offered_book_id,
        message=data.message
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer


@router.get("/my-offers", response_model=List[SwapOfferResponse])
def get_my_offers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SwapOffer).filter(SwapOffer.requester_id == current_user.id).all()


@router.get("/received", response_model=List[SwapOfferResponse])
def get_received_offers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SwapOffer).filter(SwapOffer.owner_id == current_user.id).all()


@router.put("/{offer_id}/accept", response_model=MessageResponse)
def accept_swap(offer_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    offer = db.query(SwapOffer).filter(SwapOffer.id == offer_id, SwapOffer.owner_id == current_user.id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if offer.status != "pending":
        raise HTTPException(status_code=400, detail="Offer already responded to")
    offer.status = "accepted"
    # Mark both books as unavailable
    for book_id in [offer.wanted_book_id, offer.offered_book_id]:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            book.is_available = False
    # Award eco points to both users
    for uid in [offer.requester_id, offer.owner_id]:
        user = db.query(User).filter(User.id == uid).first()
        if user:
            user.eco_points += 20
    db.commit()
    return {"message": "Swap accepted! Both books marked as exchanged. +20 eco points each 🌱"}


@router.put("/{offer_id}/reject", response_model=MessageResponse)
def reject_swap(offer_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    offer = db.query(SwapOffer).filter(SwapOffer.id == offer_id, SwapOffer.owner_id == current_user.id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    offer.status = "rejected"
    db.commit()
    return {"message": "Swap offer rejected"}
