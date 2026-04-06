# ReBook - Buying and Selling Second-Hand Books

A simple and clean web application for buying and selling second-hand books.

## 🚀 Quick Start

### First Time Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

> The database and admin user are created automatically when the server starts for the first time.

### Run the Application
```bash
# Backend Server
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload

# Frontend (new terminal)
cd frontend  
python -m http.server 8080
```

**Or use startup scripts:**
- Windows: `start.bat`
- Mac/Linux: `start.sh`


### Access the Application
- **Frontend**: http://localhost:8080
- **API Documentation**: http://localhost:8000/docs
- **Admin Login**: username `admin`, password `admin123`

## 📋 Overview

ReBook is a web-based application designed to provide a convenient, affordable, and sustainable platform for buying and selling second-hand books. The system connects buyers and sellers through a secure and user-friendly online marketplace.

## ✨ Features

### User Features
- **Authentication**: Register, login, JWT-based sessions
- **User Profile**: View and edit profile (name, email, phone, address)
- **Browse Books**: Search by title/author, filter by category and condition (with Enter key support)
- **Book Details**: Click any book card to view full details, reviews, and ratings
- **Shopping Cart**: Add/remove books, quantity management
- **Checkout**: Place orders with shipping address and payment method
- **Orders**: View order history with status tracking
- **Reviews**: Rate and review books with star ratings
- **Sell Books**: List your own books for sale

### Admin Features
- **Dashboard**: Overview of platform activity
- **User Management**: View and manage users
- **Order Management**: View and update all orders

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight embedded database
- **SQLAlchemy** - Python ORM
- **Pydantic v2** - Data validation
- **JWT (python-jose)** - Authentication tokens
- **bcrypt (passlib)** - Password hashing

### Frontend
- **HTML5 + CSS3** - Clean and responsive UI
- **Vanilla JavaScript** - No framework dependencies

## 📁 Project Structure

```
Rebook-App/
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── requirements.txt      # Python dependencies
│   └── app/
│       ├── __init__.py
│       ├── database.py       # SQLite connection & init
│       ├── models.py         # SQLAlchemy models
│       ├── schemas.py        # Pydantic schemas
│       ├── auth.py           # JWT auth & password hashing
│       └── routes/
│           ├── routes_auth.py    # Register, login, profile
│           ├── routes_books.py   # Book CRUD & search
│           ├── routes_cart.py    # Shopping cart
│           ├── routes_orders.py  # Order management
│           ├── routes_reviews.py # Book reviews & ratings
│           └── routes_admin.py   # Admin endpoints
├── frontend/
│   ├── index.html            # Single page application
│   ├── css/
│   │   └── style.css         # Responsive styling
│   └── js/
│       └── app.js            # All frontend logic
├── start.bat                 # Windows startup script
├── start.sh                  # Mac/Linux startup script
└── README.md
```

## 🔌 API Endpoints

All endpoints are prefixed with `/api`.

### Authentication (`/api/auth`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login (returns JWT token) |
| GET | `/api/auth/me` | Get current user profile |
| PUT | `/api/auth/me` | Update current user profile |

### Books (`/api/books`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books` | List books (search, category, condition filters) |
| GET | `/api/books/{id}` | Get book details with seller info |
| POST | `/api/books` | List a book for sale (authenticated) |
| PUT | `/api/books/{id}` | Update a book (owner only) |
| DELETE | `/api/books/{id}` | Delete a book (owner only) |
| GET | `/api/books/my-books` | Get current user's listed books |

### Cart (`/api/cart`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart` | Get user's cart items |
| POST | `/api/cart` | Add item to cart |
| DELETE | `/api/cart/{id}` | Remove item from cart |

### Orders (`/api/orders`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | Get user's orders |
| GET | `/api/orders/{id}` | Get order details |
| POST | `/api/orders` | Place order from cart |

### Reviews (`/api/reviews`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reviews/book/{book_id}` | Get reviews for a book |
| GET | `/api/reviews/book/{book_id}/average-rating` | Get average rating |
| POST | `/api/reviews` | Submit a review (authenticated) |

### Admin (`/api/admin`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users` | List all users |
| GET | `/api/admin/orders` | List all orders |
| PUT | `/api/admin/orders/{id}` | Update order status |

## 🗄️ Database Schema

- **User**: id, email, username, hashed_password, full_name, phone, address, is_admin, is_active, created_at
- **Book**: id, title, author, isbn, category, condition, price, description, image_url, is_available, seller_id, created_at
- **CartItem**: id, user_id, book_id, quantity, added_at
- **Order**: id, user_id, total_amount, shipping_address, payment_method, status, created_at
- **OrderItem**: id, order_id, book_id, quantity, price_at_purchase
- **Review**: id, book_id, user_id, rating, comment, created_at

## 📝 Development Guidelines

### Code Quality
- **DRY Principle**: Eliminate duplication
- **Clean Code**: Clear naming, small functions
- **Type Hints**: Use Pydantic schemas
- **Error Handling**: Proper status codes and messages

### Security
- **Password Hashing**: bcrypt via passlib
- **JWT Tokens**: Secure authentication
- **Input Validation**: Pydantic v2 schemas
- **SQL Injection Prevention**: SQLAlchemy ORM

## 🔧 Troubleshooting

### Dependency Installation Issues
If `cryptography` or `bcrypt` fails to install on Windows:
```bash
# Option 1: Use pre-built wheels
pip install cryptography --only-binary :all:

# Option 2: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### Database Issues
```bash
# Reset database — just delete the file and restart the server
cd backend
del rebook.db
# The database and admin user are recreated on next server start
python -m uvicorn main:app --reload
```

### Port Already in Use
```bash
# Change ports or use:
python -m uvicorn main:app --port 8001
python -m http.server 8081
```

## 🎯 Key Objectives

1. **Simplify Book Buying/Selling**: Intuitive platform for all users
2. **Centralized Management**: Unified system for monitoring and management
3. **Enhance Communication**: Clear notifications and order tracking
4. **Promote Sustainability**: Reduce waste through book reuse
5. **Secure Transactions**: Safe and reliable payment processing

## 👥 Target Users

- Students (schools, colleges, universities)
- Book lovers and readers
- Libraries and study centers
- Local bookstores
- General public interested in affordable books

## 📄 License

MIT License - See LICENSE file for details

## 📞 Contact

For questions or support, please open an issue on GitHub.
