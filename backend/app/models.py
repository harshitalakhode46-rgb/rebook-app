"""
Database Models for ReBook
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    eco_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    books = relationship("Book", back_populates="seller", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="buyer", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")
    swap_offers_sent = relationship("SwapOffer", foreign_keys="SwapOffer.requester_id", back_populates="requester", cascade="all, delete-orphan")
    swap_offers_received = relationship("SwapOffer", foreign_keys="SwapOffer.owner_id", back_populates="owner", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    category = Column(String(100), index=True)
    isbn = Column(String(20))
    description = Column(Text)
    condition = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String(500))
    is_available = Column(Boolean, default=True)
    swap_available = Column(Boolean, default=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    seller = relationship("User", back_populates="books")
    order_items = relationship("OrderItem", back_populates="book")
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="book", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="cart_items")
    book = relationship("Book")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
    shipping_address = Column(Text, nullable=False)
    payment_method = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    buyer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    book = relationship("Book", back_populates="order_items")


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Wishlist(Base):
    __tablename__ = "wishlist"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="wishlist_items")
    book = relationship("Book", back_populates="wishlist_items")


class SwapOffer(Base):
    __tablename__ = "swap_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wanted_book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    offered_book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    message = Column(Text)
    status = Column(String(20), default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    requester = relationship("User", foreign_keys=[requester_id], back_populates="swap_offers_sent")
    owner = relationship("User", foreign_keys=[owner_id], back_populates="swap_offers_received")
    wanted_book = relationship("Book", foreign_keys=[wanted_book_id])
    offered_book = relationship("Book", foreign_keys=[offered_book_id])
