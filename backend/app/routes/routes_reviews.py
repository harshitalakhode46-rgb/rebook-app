"""
Review and Rating Routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Review, Book, User
from app.schemas import ReviewCreate, ReviewResponse, MessageResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/reviews")


@router.get("/book/{book_id}", response_model=List[ReviewResponse])
def get_book_reviews(
    book_id: int,
    db: Session = Depends(get_db)
):
    """Get all reviews for a specific book"""
    # Check if book exists
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return reviews


@router.get("/book/{book_id}/average-rating")
def get_book_average_rating(
    book_id: int,
    db: Session = Depends(get_db)
):
    """Get average rating for a book"""
    result = db.query(
        func.avg(Review.rating).label("average"),
        func.count(Review.id).label("count")
    ).filter(Review.book_id == book_id).first()
    
    return {
        "book_id": book_id,
        "average_rating": round(result.average, 2) if result.average else 0,
        "total_reviews": result.count
    }


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a review for a book"""
    # Check if book exists
    book = db.query(Book).filter(Book.id == review_data.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check if user already reviewed this book
    existing_review = db.query(Review).filter(
        Review.book_id == review_data.book_id,
        Review.user_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this book"
        )
    
    # Create review
    new_review = Review(
        book_id=review_data.book_id,
        user_id=current_user.id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.delete("/{review_id}", response_model=MessageResponse)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check if user owns the review or is admin
    if review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}
