"""
Pydantic Schemas for Request/Response Validation
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    eco_points: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    category: str
    isbn: Optional[str] = None
    description: Optional[str] = None
    condition: str
    price: float = Field(gt=0)
    image_url: Optional[str] = None
    swap_available: Optional[bool] = False


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    swap_available: Optional[bool] = None


class BookResponse(BookBase):
    id: int
    seller_id: int
    is_available: bool
    swap_available: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BookWithSeller(BookResponse):
    seller: UserResponse


# Cart Schemas
class CartItemCreate(BaseModel):
    book_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    id: int
    book_id: int
    quantity: int
    added_at: datetime
    book: BookResponse
    
    model_config = ConfigDict(from_attributes=True)


# Order Schemas
class OrderItemCreate(BaseModel):
    book_id: int
    quantity: int


class OrderCreate(BaseModel):
    shipping_address: str
    payment_method: str
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    book_id: int
    quantity: int
    price: float
    book: BookResponse
    
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    total_amount: float
    status: str
    shipping_address: str
    payment_method: Optional[str] = None
    created_at: datetime
    items: List[OrderItemResponse]
    
    model_config = ConfigDict(from_attributes=True)


# Review Schemas
class ReviewCreate(BaseModel):
    book_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)


# Wishlist Schemas
class WishlistResponse(BaseModel):
    id: int
    book_id: int
    added_at: datetime
    book: BookResponse
    
    model_config = ConfigDict(from_attributes=True)


# Swap Schemas
class SwapOfferCreate(BaseModel):
    wanted_book_id: int
    offered_book_id: int
    message: Optional[str] = None


class SwapOfferResponse(BaseModel):
    id: int
    requester_id: int
    owner_id: int
    wanted_book: BookResponse
    offered_book: BookResponse
    requester: UserResponse
    message: Optional[str]
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# General Response
class MessageResponse(BaseModel):
    message: str

