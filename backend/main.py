"""
ReBook - Main FastAPI Application
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.database import init_db, engine
from app.routes.routes_auth import router as auth_router
from app.routes.routes_books import router as books_router
from app.routes.routes_cart import router as cart_router
from app.routes.routes_orders import router as orders_router
from app.routes.routes_reviews import router as reviews_router
from app.routes.routes_admin import router as admin_router
from app.routes.routes_wishlist import router as wishlist_router
from app.routes.routes_swap import router as swap_router
from app.routes.routes_extras import router as extras_router
from app.routes.routes_capsule import router as capsule_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import SessionLocal
    from app.models import User
    from app.auth import hash_password
    from sqlalchemy import text

    init_db()

    # Migrate new columns (safe - ignores if already exists)
    with engine.connect() as conn:
        for sql in [
            "ALTER TABLE users ADD COLUMN eco_points INTEGER DEFAULT 0",
            "ALTER TABLE books ADD COLUMN swap_available BOOLEAN DEFAULT 0",
            "CREATE TABLE IF NOT EXISTS book_memories (id INTEGER PRIMARY KEY, book_id INTEGER UNIQUE NOT NULL REFERENCES books(id), memory TEXT NOT NULL, year_read INTEGER, mood_tag VARCHAR(50), created_at DATETIME DEFAULT CURRENT_TIMESTAMP)",
            "CREATE TABLE IF NOT EXISTS reading_chain (id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id), user_id INTEGER NOT NULL REFERENCES users(id), note TEXT, city VARCHAR(100), read_at DATETIME DEFAULT CURRENT_TIMESTAMP)",
        ]:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                pass

    print("[OK] Database ready")

    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.email == "admin@rebook.com").first()
        if not existing_admin:
            admin = User(
                email="admin@rebook.com",
                username="admin",
                hashed_password=hash_password("admin123"),
                full_name="Admin User",
                is_admin=True,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("[OK] Admin user created: admin / admin123")
        else:
            print("[INFO] Admin user already exists")
    except Exception as e:
        print(f"[WARN] Admin creation: {e}")
        db.rollback()
    finally:
        db.close()

    yield


app = FastAPI(
    title="ReBook API",
    description="API for buying and selling second-hand books.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,     tags=["1. Authentication"])
app.include_router(books_router,    tags=["2. Books"])
app.include_router(cart_router,     tags=["3. Shopping Cart"])
app.include_router(orders_router,   tags=["4. Orders"])
app.include_router(reviews_router,  tags=["5. Reviews"])
app.include_router(admin_router,    tags=["6. Admin"])
app.include_router(wishlist_router, tags=["7. Wishlist"])
app.include_router(swap_router,     tags=["8. Book Swap"])
app.include_router(extras_router,   tags=["9. Extras"])
app.include_router(capsule_router,  tags=["10. Time Capsule & Reading Chain"])


@app.get("/")
def root():
    return {"message": "Welcome to ReBook API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
