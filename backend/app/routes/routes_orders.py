"""
Order Management Routes
"""
import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, OrderItem, Book, CartItem, User
from app.schemas import OrderCreate, OrderResponse, MessageResponse
from app.auth import get_current_user

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

router = APIRouter(prefix="/api/orders")


@router.get("", response_model=List[OrderResponse])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all orders for current user"""
    orders = db.query(Order).filter(Order.buyer_id == current_user.id).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.buyer_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new order from cart or specific items"""
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    # Calculate total and validate books
    total_amount = 0
    order_items = []
    
    for item in order_data.items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book {item.book_id} not found"
            )
        if not book.is_available:
            # Auto-remove unavailable book from cart and skip
            db.query(CartItem).filter(
                CartItem.user_id == current_user.id,
                CartItem.book_id == item.book_id
            ).delete(synchronize_session=False)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{book.title}' is no longer available and has been removed from your cart. Please review your cart."
            )
        
        item_total = book.price * item.quantity
        total_amount += item_total
        order_items.append({
            "book_id": book.id,
            "quantity": item.quantity,
            "price": book.price
        })
    
    # Create order
    new_order = Order(
        buyer_id=current_user.id,
        total_amount=total_amount,
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method,
        status="pending"
    )
    db.add(new_order)
    db.flush()  # Get order ID
    
    # Create order items
    for item_data in order_items:
        order_item = OrderItem(
            order_id=new_order.id,
            **item_data
        )
        db.add(order_item)
        
        # Mark book as unavailable
        book = db.query(Book).filter(Book.id == item_data["book_id"]).first()
        book.is_available = False
    
    # Clear cart items for purchased books
    book_ids = [item["book_id"] for item in order_items]
    db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.book_id.in_(book_ids)
    ).delete(synchronize_session=False)
    
    db.commit()
    db.refresh(new_order)
    # Award eco points to buyer (+5 per order)
    current_user.eco_points = (current_user.eco_points or 0) + 5
    db.commit()
    return new_order


@router.post("/create-razorpay-order")
def create_razorpay_order(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a Razorpay order from current cart total"""
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item.book.price * item.quantity for item in cart_items)
    amount_paise = int(total * 100)

    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Razorpay is not configured. Please add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in backend/.env file. Get your test keys from https://dashboard.razorpay.com"
        )

    try:
        import razorpay
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        rz_order = razorpay_client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })
        return {
            "razorpay_order_id": rz_order["id"],
            "amount": amount_paise,
            "currency": "INR",
            "key": RAZORPAY_KEY_ID
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Razorpay error: {str(e)}")


@router.put("/{order_id}/cancel", response_model=MessageResponse)
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel an order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.buyer_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status not in ["pending", "confirmed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel order at this stage"
        )
    
    # Update order status
    order.status = "cancelled"
    
    # Make books available again
    for item in order.items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        if book:
            book.is_available = True
    
    db.commit()
    return {"message": "Order cancelled successfully"}
