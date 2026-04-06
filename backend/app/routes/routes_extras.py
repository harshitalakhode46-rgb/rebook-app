"""
Price Suggester + Eco Points / Badges
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Book, User, Order
from app.auth import get_current_user

router = APIRouter(prefix="/api/extras")

BADGES = [
    {"id": "first_buy",    "icon": "🛒", "label": "First Purchase",   "desc": "Bought your first book"},
    {"id": "bookworm",     "icon": "📚", "label": "Bookworm",          "desc": "Bought 5+ books"},
    {"id": "first_sell",   "icon": "💰", "label": "First Sale",        "desc": "Sold your first book"},
    {"id": "top_seller",   "icon": "🏆", "label": "Top Seller",        "desc": "Sold 5+ books"},
    {"id": "eco50",        "icon": "🌱", "label": "Eco Warrior",       "desc": "Earned 50+ eco points"},
    {"id": "eco100",       "icon": "🌍", "label": "Planet Saver",      "desc": "Earned 100+ eco points"},
    {"id": "swapper",      "icon": "🔄", "label": "Book Swapper",      "desc": "Completed a book swap"},
    {"id": "reviewer",     "icon": "⭐", "label": "Critic",            "desc": "Wrote 3+ reviews"},
]


@router.get("/price-suggest")
def suggest_price(title: str = Query(...), db: Session = Depends(get_db)):
    results = db.query(func.avg(Book.price), func.min(Book.price), func.max(Book.price), func.count(Book.id))\
        .filter(Book.title.ilike(f"%{title}%")).first()
    avg, mn, mx, cnt = results
    if not cnt:
        return {"found": False, "message": "No similar books found. Set your own price!"}
    return {
        "found": True,
        "count": cnt,
        "avg_price": round(avg, 2),
        "min_price": round(mn, 2),
        "max_price": round(mx, 2),
        "suggested_price": round(avg * 0.85, 2)
    }


@router.get("/my-badges")
def get_my_badges(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bought = db.query(Order).filter(Order.buyer_id == current_user.id).count()
    sold = db.query(Book).filter(Book.seller_id == current_user.id, Book.is_available == False).count()
    from app.models import Review, SwapOffer
    reviews = db.query(Review).filter(Review.user_id == current_user.id).count()
    swaps = db.query(SwapOffer).filter(
        ((SwapOffer.requester_id == current_user.id) | (SwapOffer.owner_id == current_user.id)),
        SwapOffer.status == "accepted"
    ).count()

    earned = []
    if bought >= 1:  earned.append("first_buy")
    if bought >= 5:  earned.append("bookworm")
    if sold >= 1:    earned.append("first_sell")
    if sold >= 5:    earned.append("top_seller")
    if current_user.eco_points >= 50:  earned.append("eco50")
    if current_user.eco_points >= 100: earned.append("eco100")
    if swaps >= 1:   earned.append("swapper")
    if reviews >= 3: earned.append("reviewer")

    badges = [b for b in BADGES if b["id"] in earned]
    return {
        "eco_points": current_user.eco_points,
        "badges": badges,
        "stats": {"bought": bought, "sold": sold, "reviews": reviews, "swaps": swaps}
    }


@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.eco_points > 0, User.is_active == True)\
        .order_by(User.eco_points.desc()).limit(10).all()
    return [{"rank": i+1, "username": u.username, "full_name": u.full_name, "eco_points": u.eco_points}
            for i, u in enumerate(users)]
