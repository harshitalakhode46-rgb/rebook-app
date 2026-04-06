"""
Admin Routes - User and Book Management
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Book, Order
from app.schemas import UserResponse, BookResponse, OrderResponse, MessageResponse
from app.auth import get_current_admin_user

router = APIRouter(prefix="/api/admin")


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 50,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (Admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.put("/users/{user_id}/toggle-active", response_model=MessageResponse)
def toggle_user_active(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Activate or deactivate a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = not user.is_active
    db.commit()
    
    status_text = "activated" if user.is_active else "deactivated"
    return {"message": f"User {status_text} successfully"}


@router.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete admin users"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.get("/books", response_model=List[BookResponse])
def get_all_books(
    skip: int = 0,
    limit: int = 50,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all books including unavailable (Admin only)"""
    books = db.query(Book).offset(skip).limit(limit).all()
    return books


@router.delete("/books/{book_id}", response_model=MessageResponse)
def admin_delete_book(
    book_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete any book (Admin only)"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    skip: int = 0,
    limit: int = 50,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all orders (Admin only)"""
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@router.put("/orders/{order_id}/status", response_model=MessageResponse)
def update_order_status(
    order_id: int,
    status: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update order status (Admin only)"""
    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = status
    db.commit()
    return {"message": f"Order status updated to {status}"}


@router.get("/stats")
def get_platform_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get platform statistics (Admin only)"""
    total_users = db.query(User).count()
    total_books = db.query(Book).count()
    available_books = db.query(Book).filter(Book.is_available == True).count()
    total_orders = db.query(Order).count()
    
    return {
        "total_users": total_users,
        "total_books": total_books,
        "available_books": available_books,
        "sold_books": total_books - available_books,
        "total_orders": total_orders
    }
