// ReBook Frontend JavaScript

const API_URL = 'http://localhost:8000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;

function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function getToken() {
    if (!authToken) authToken = localStorage.getItem('authToken');
    return authToken;
}

function setToken(token) {
    authToken = token;
    if (token) localStorage.setItem('authToken', token);
    else localStorage.removeItem('authToken');
}

async function authFetch(url, options = {}) {
    const token = getToken();
    if (!token) return null;
    const headers = { ...(options.headers || {}), 'Authorization': `Bearer ${token}` };
    return fetch(url, { ...options, headers });
}

async function fetchCurrentUser() {
    try {
        const response = await authFetch(`${API_URL}/auth/me`);
        if (response && response.ok) {
            currentUser = await response.json();
            return true;
        }
    } catch (e) {}
    try {
        const payload = JSON.parse(atob(getToken().split('.')[1]));
        currentUser = { username: payload.sub, full_name: payload.sub };
    } catch (_) {}
    return false;
}

document.addEventListener('DOMContentLoaded', async () => {
    if (getToken()) {
        await fetchCurrentUser();
        setupAuthenticatedUI();
    }
    loadBooks();
    updateCartCount();

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') { e.preventDefault(); loadBooks(); }
        });
    }
});

function showSection(sectionId) {
    if (['sell', 'myBooks', 'cart', 'orders', 'profile', 'checkout', 'dashboard', 'wishlist', 'swap'].includes(sectionId) && !getToken()) {
        showAlert('Please login to access this feature', 'error');
        sectionId = 'login';
    }
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');

    if (sectionId === 'books') loadBooks();
    else if (sectionId === 'cart') loadCart();
    else if (sectionId === 'orders') loadOrders();
    else if (sectionId === 'myBooks') loadMyBooks();
    else if (sectionId === 'profile') loadProfile();
    else if (sectionId === 'checkout') loadCheckout();
    else if (sectionId === 'dashboard') loadDashboard();
    else if (sectionId === 'wishlist') loadWishlist();
    else if (sectionId === 'swap') loadSwapBooks();
    else if (sectionId === 'leaderboard') loadLeaderboard();
}

function setupAuthenticatedUI() {
    document.getElementById('navAuth').style.display = 'none';
    document.getElementById('navUser').style.display = 'flex';
    document.querySelector('.nav-sell').style.display = 'block';
    document.querySelector('.nav-mybooks').style.display = 'block';
    document.querySelector('.nav-wishlist').style.display = 'block';
    document.querySelector('.nav-swap').style.display = 'block';
    document.getElementById('userName').textContent =
        (currentUser && (currentUser.full_name || currentUser.username)) || '';
    if (currentUser && currentUser.is_admin) {
        document.querySelector('.nav-dashboard').style.display = 'block';
    }
}

function resetToLoggedOutUI() {
    document.getElementById('navAuth').style.display = 'flex';
    document.getElementById('navUser').style.display = 'none';
    document.querySelector('.nav-sell').style.display = 'none';
    document.querySelector('.nav-mybooks').style.display = 'none';
    document.querySelector('.nav-wishlist').style.display = 'none';
    document.querySelector('.nav-swap').style.display = 'none';
    document.querySelector('.nav-dashboard').style.display = 'none';
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    const main = document.querySelector('main');
    main.insertBefore(alertDiv, main.firstChild);
    setTimeout(() => alertDiv.remove(), 5000);
}

async function handleRegister(event) {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.target));
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            showAlert('Registration successful! Please login.', 'success');
            showSection('login');
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Registration failed', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

async function handleLogin(event) {
    event.preventDefault();
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: new FormData(event.target)
        });
        if (response.ok) {
            const data = await response.json();
            setToken(data.access_token);
            await fetchCurrentUser();
            setupAuthenticatedUI();
            showAlert('Login successful!', 'success');
            showSection('home');
        } else {
            showAlert('Invalid username or password', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

function logout() {
    setToken(null);
    currentUser = null;
    resetToLoggedOutUI();
    showAlert('Logged out successfully', 'success');
    showSection('home');
}

async function loadBooks() {
    const search = document.getElementById('searchInput')?.value || '';
    const category = document.getElementById('categoryFilter')?.value || '';
    const condition = document.getElementById('conditionFilter')?.value || '';

    let url = `${API_URL}/books?`;
    if (search) url += `search=${encodeURIComponent(search)}&`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    if (condition) url += `condition=${encodeURIComponent(condition)}&`;

    try {
        const response = await fetch(url);
        const books = await response.json();
        displayBooks(books);
    } catch (e) {
        showAlert('Failed to load books', 'error');
    }
}

function bookImageHtml(image_url, cls = 'book-img') {
    if (!image_url) return '';
    const src = image_url.startsWith('http') ? image_url : `http://localhost:8000/${image_url}`;
    return `<img src="${src}" class="${cls}" onerror="this.style.display='none'">`;
}

function displayBooks(books) {
    const grid = document.getElementById('booksGrid');
    if (books.length === 0) {
        grid.innerHTML = '<p>No books found.</p>';
        return;
    }
    grid.innerHTML = books.map(book => `
        <div class="book-card" onclick="viewBookDetail(${book.id})" style="cursor:pointer;">
            ${bookImageHtml(book.image_url)}
            <div class="book-card-body">
                <h3>${escapeHtml(book.title)}</h3>
                <p class="author">by ${escapeHtml(book.author)}</p>
                <div class="book-card-meta">
                    <span class="category">${escapeHtml(book.category)}</span>
                    <span class="condition-badge">${escapeHtml(book.condition.replace('_', ' '))}</span>
                    ${book.swap_available ? '<span class="swap-badge">🔄 Swap</span>' : ''}
                </div>
                ${book.description ? `<p class="book-desc">${escapeHtml(book.description.substring(0, 80))}...</p>` : ''}
            </div>
            <div class="book-card-footer">
                <p class="price">&#8377;${book.price.toFixed(2)}</p>
                <div style="display:flex;gap:0.4rem;">
                    <button onclick="event.stopPropagation(); toggleWishlist(${book.id}, this)" class="btn-wishlist" title="Add to Wishlist">❤️</button>
                    <button onclick="event.stopPropagation(); addToCart(${book.id})" class="btn-add-cart">🛒 Cart</button>
                </div>
            </div>
        </div>
    `).join('');
}

async function handleSellBook(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const bookData = {
        title: formData.get('title'),
        author: formData.get('author'),
        category: formData.get('category'),
        price: parseFloat(formData.get('price')),
        description: formData.get('description'),
        condition: formData.get('condition'),
        swap_available: formData.get('swap_available') === 'on'
    };
    const sendData = new FormData();
    sendData.append('book_data', JSON.stringify(bookData));
    sendData.append('image', formData.get('image'));

    try {
        const response = await fetch(`${API_URL}/books`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${getToken()}` },
            body: sendData
        });
        if (response.ok) {
            showAlert('Book listed successfully! +10 🌱 Eco Points earned!', 'success');
            event.target.reset();
            showSection('myBooks');
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Failed to list book', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

async function suggestPrice() {
    const title = document.querySelector('input[name="title"]').value.trim();
    if (!title) { showAlert('Enter book title first to get price suggestion', 'error'); return; }
    try {
        const res = await fetch(`${API_URL}/extras/price-suggest?title=${encodeURIComponent(title)}`);
        const data = await res.json();
        if (data.found) {
            document.querySelector('input[name="price"]').value = data.suggested_price;
            showAlert(`💡 Price suggested: ₹${data.suggested_price} (based on ${data.count} similar books, avg ₹${data.avg_price})`, 'success');
        } else {
            showAlert('No similar books found. Set your own price!', 'info');
        }
    } catch (e) { showAlert('Could not fetch suggestion', 'error'); }
}

async function loadMyBooks() {
    if (!getToken()) { showSection('login'); return; }
    try {
        const response = await authFetch(`${API_URL}/books/seller/my-books`);
        if (response && response.ok) {
            displayMyBooks(await response.json());
        } else {
            showAlert('Failed to load your books', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

function displayMyBooks(books) {
    const grid = document.getElementById('myBooksGrid');
    if (books.length === 0) {
        grid.innerHTML = '<p>You haven\'t listed any books yet. <a href="#" onclick="showSection(\'sell\')">Sell your first book</a></p>';
        return;
    }
    grid.innerHTML = books.map(book => `
        <div class="book-card" onclick="viewBookDetail(${book.id})" style="cursor:pointer;">
            ${bookImageHtml(book.image_url)}
            <div class="book-card-body">
                <h3>${escapeHtml(book.title)}</h3>
                <p class="author">by ${escapeHtml(book.author)}</p>
                <div class="book-card-meta">
                    <span class="category">${escapeHtml(book.category)}</span>
                    <span class="condition-badge">${escapeHtml(book.condition.replace('_', ' '))}</span>
                </div>
                ${book.description ? `<p class="book-desc">${escapeHtml(book.description.substring(0, 80))}...</p>` : ''}
            </div>
            <div class="book-card-footer">
                <p class="price">&#8377;${book.price.toFixed(2)}</p>
                <span class="status ${book.is_available ? 'available' : 'sold'}">
                    ${book.is_available ? 'Available' : 'Sold'}
                </span>
            </div>
            ${book.is_available ? `
            <div class="book-actions">
                <button onclick="event.stopPropagation(); deleteBook(${book.id})" class="btn-secondary">Delete</button>
            </div>` : ''}
        </div>
    `).join('');
}

async function deleteBook(bookId) {
    if (!confirm('Are you sure you want to delete this book?')) return;
    try {
        const response = await authFetch(`${API_URL}/books/${bookId}`, { method: 'DELETE' });
        if (response && response.ok) {
            showAlert('Book deleted successfully', 'success');
            loadMyBooks();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Failed to delete book', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

async function addToCart(bookId) {
    if (!getToken()) {
        showAlert('Please login to add items to cart', 'error');
        showSection('login');
        return;
    }
    try {
        const response = await authFetch(`${API_URL}/cart`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ book_id: bookId, quantity: 1 })
        });
        if (response && response.ok) {
            showAlert('Book added to cart!', 'success');
            updateCartCount();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Failed to add to cart', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

async function loadCart() {
    if (!getToken()) {
        document.getElementById('cartItems').innerHTML = '<p>Please login to view your cart.</p>';
        return;
    }
    try {
        const response = await authFetch(`${API_URL}/cart`);
        if (response && response.ok) {
            const items = await response.json();
            displayCart(items);
            updateCartCount();
        }
    } catch (e) {
        showAlert('Failed to load cart', 'error');
    }
}

function displayCart(items) {
    const cartDiv = document.getElementById('cartItems');
    const summaryDiv = document.getElementById('cartSummary');
    if (items.length === 0) {
        cartDiv.innerHTML = '<p>Your cart is empty.</p>';
        summaryDiv.style.display = 'none';
        return;
    }
    let total = 0;
    cartDiv.innerHTML = items.map(item => {
        total += item.book.price * item.quantity;
        return `
            <div class="cart-item">
                <div>
                    <h3>${escapeHtml(item.book.title)}</h3>
                    <p>by ${escapeHtml(item.book.author)}</p>
                    <p>Quantity: ${item.quantity}</p>
                </div>
                <div>
                    <p class="price">&#8377;${(item.book.price * item.quantity).toFixed(2)}</p>
                    <button onclick="removeFromCart(${item.id})" class="btn-danger">Remove</button>
                </div>
            </div>`;
    }).join('');
    document.getElementById('cartTotal').textContent = total.toFixed(2);
    summaryDiv.style.display = 'block';
}

async function removeFromCart(itemId) {
    try {
        const response = await authFetch(`${API_URL}/cart/${itemId}`, { method: 'DELETE' });
        if (response && response.ok) {
            showAlert('Item removed from cart', 'success');
            loadCart();
            updateCartCount();
        }
    } catch (e) {
        showAlert('Failed to remove item', 'error');
    }
}

async function updateCartCount() {
    if (!getToken()) return;
    try {
        const response = await authFetch(`${API_URL}/cart`);
        if (response && response.ok) {
            const items = await response.json();
            document.getElementById('cartCount').textContent = items.length;
        }
    } catch (e) {}
}

async function loadCheckout() {
    if (!getToken()) { showSection('login'); return; }
    try {
        const response = await authFetch(`${API_URL}/cart`);
        if (!response || !response.ok) { showAlert('Failed to load cart', 'error'); showSection('cart'); return; }
        const items = await response.json();
        if (items.length === 0) { showAlert('Your cart is empty', 'error'); showSection('cart'); return; }

        let total = 0;
        document.getElementById('checkoutItemsList').innerHTML =
            '<div class="checkout-items">' +
            items.map(item => {
                const t = item.book.price * item.quantity;
                total += t;
                return `<div class="checkout-item">
                    <span>${escapeHtml(item.book.title)} x ${item.quantity}</span>
                    <span>&#8377;${t.toFixed(2)}</span>
                </div>`;
            }).join('') +
            '</div>';
        document.getElementById('checkoutTotalAmount').textContent = total.toFixed(2);
    } catch (e) {
        showAlert('Failed to load checkout', 'error');
        showSection('cart');
    }
}

async function handleCheckout(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const shippingAddress = formData.get('shipping_address');
    const paymentMethod = formData.get('payment_method');
    if (!shippingAddress || !paymentMethod) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    if (paymentMethod === 'razorpay') {
        await handleRazorpayCheckout(shippingAddress);
        return;
    }

    // COD flow
    try {
        const cartResponse = await authFetch(`${API_URL}/cart`);
        if (!cartResponse || !cartResponse.ok) { showAlert('Failed to load cart', 'error'); return; }
        const cartItems = await cartResponse.json();
        if (cartItems.length === 0) { showAlert('Your cart is empty', 'error'); showSection('cart'); return; }

        const response = await authFetch(`${API_URL}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                shipping_address: shippingAddress,
                payment_method: 'Cash on Delivery',
                items: cartItems.map(item => ({ book_id: item.book_id, quantity: item.quantity }))
            })
        });
        if (response && response.ok) {
            const order = await response.json();
            showAlert('Order placed successfully! Order #' + order.id, 'success');
            showSection('orders');
            updateCartCount();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Failed to create order', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

async function handleRazorpayCheckout(shippingAddress) {
    // Get cart items first
    const cartResponse = await authFetch(`${API_URL}/cart`);
    if (!cartResponse || !cartResponse.ok) { showAlert('Failed to load cart', 'error'); return; }
    const cartItems = await cartResponse.json();
    if (!cartItems.length) { showAlert('Your cart is empty', 'error'); showSection('cart'); return; }

    const total = cartItems.reduce((sum, item) => sum + item.book.price * item.quantity, 0);
    showSimulatedPayment(total, shippingAddress, cartItems);
}

function showSimulatedPayment(total, shippingAddress, cartItems) {
    const overlay = document.createElement('div');
    overlay.id = 'paymentOverlay';
    overlay.innerHTML = `
        <div class="payment-modal">
            <div class="payment-header">
                <img src="https://razorpay.com/favicon.ico" style="height:20px;vertical-align:middle;margin-right:8px;">Razorpay Secure Checkout
            </div>
            <div class="payment-body" id="paymentBody">
                <div class="payment-amount">₹${total.toFixed(2)}</div>
                <p style="color:#666;font-size:0.9rem;margin-bottom:1.5rem;">ReBook — Second-Hand Books Purchase</p>

                <div class="payment-tabs">
                    <button class="pay-tab active" onclick="switchPayTab('card', this)">💳 Card</button>
                    <button class="pay-tab" onclick="switchPayTab('upi', this)">📱 UPI</button>
                    <button class="pay-tab" onclick="switchPayTab('netbanking', this)">🏦 Net Banking</button>
                </div>

                <div id="payTab-card" class="pay-tab-content active">
                    <input class="pay-input" type="text" placeholder="Card Number" maxlength="19"
                        oninput="this.value=this.value.replace(/[^0-9]/g,'').replace(/(.{4})/g,'$1 ').trim()">
                    <div style="display:flex;gap:0.75rem;">
                        <input class="pay-input" type="text" placeholder="MM / YY" maxlength="7" style="flex:1">
                        <input class="pay-input" type="text" placeholder="CVV" maxlength="3" style="flex:1">
                    </div>
                    <input class="pay-input" type="text" placeholder="Name on Card">
                </div>

                <div id="payTab-upi" class="pay-tab-content">
                    <input class="pay-input" type="text" placeholder="Enter UPI ID (e.g. name@upi)">
                    <p style="font-size:0.8rem;color:#888;">You will receive a payment request on your UPI app</p>
                </div>

                <div id="payTab-netbanking" class="pay-tab-content">
                    <select class="pay-input">
                        <option value="">Select Your Bank</option>
                        <option>State Bank of India</option>
                        <option>HDFC Bank</option>
                        <option>ICICI Bank</option>
                        <option>Axis Bank</option>
                        <option>Kotak Mahindra Bank</option>
                        <option>Punjab National Bank</option>
                    </select>
                </div>

                <button class="pay-btn" onclick="processSimulatedPayment('${shippingAddress.replace(/'/g, "\\'")}')">Pay ₹${total.toFixed(2)}</button>
                <button class="pay-cancel" onclick="document.getElementById('paymentOverlay').remove()">Cancel</button>
            </div>
        </div>`;
    document.body.appendChild(overlay);
}

function switchPayTab(tab, btn) {
    document.querySelectorAll('.pay-tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.pay-tab').forEach(b => b.classList.remove('active'));
    document.getElementById('payTab-' + tab).classList.add('active');
    btn.classList.add('active');
}

async function processSimulatedPayment(shippingAddress) {
    const body = document.getElementById('paymentBody');
    body.innerHTML = `
        <div style="text-align:center;padding:2rem 1rem;">
            <div class="pay-spinner"></div>
            <p style="margin-top:1rem;color:#555;">Processing payment...</p>
        </div>`;

    await new Promise(r => setTimeout(r, 2000));

    const paymentId = 'pay_SIM' + Math.random().toString(36).substr(2, 14).toUpperCase();

    body.innerHTML = `
        <div style="text-align:center;padding:1.5rem 1rem;">
            <div style="font-size:3rem;">✅</div>
            <h3 style="color:#27ae60;margin:0.5rem 0;">Payment Successful!</h3>
            <p style="color:#666;font-size:0.85rem;">Payment ID: <code>${paymentId}</code></p>
            <p style="color:#888;font-size:0.8rem;">Placing your order...</p>
        </div>`;

    await new Promise(r => setTimeout(r, 1200));

    // Place order
    const cartResponse = await authFetch(`${API_URL}/cart`);
    const cartItems = await cartResponse.json();
    const orderRes = await authFetch(`${API_URL}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            shipping_address: shippingAddress,
            payment_method: 'Online Payment | ' + paymentId,
            items: cartItems.map(item => ({ book_id: item.book_id, quantity: item.quantity }))
        })
    });

    document.getElementById('paymentOverlay').remove();

    if (orderRes && orderRes.ok) {
        const order = await orderRes.json();
        showAlert('🎉 Payment successful! Order #' + order.id + ' placed.', 'success');
        showSection('orders');
        updateCartCount();
    } else {
        showAlert('Payment done but order failed. Please contact support.', 'error');
    }
}

async function loadOrders() {
    if (!getToken()) {
        document.getElementById('ordersList').innerHTML = '<p>Please login to view your orders.</p>';
        return;
    }
    try {
        const response = await authFetch(`${API_URL}/orders`);
        if (response && response.ok) {
            displayOrders(await response.json());
        } else {
            showAlert('Failed to load orders', 'error');
        }
    } catch (e) {
        showAlert('Failed to load orders', 'error');
    }
}

function displayOrders(orders) {
    const ordersDiv = document.getElementById('ordersList');
    if (orders.length === 0) {
        ordersDiv.innerHTML = '<p>No orders yet.</p>';
        return;
    }
    ordersDiv.innerHTML = orders.map(order => `
        <div class="order-card">
            <h3>Order #${order.id}</h3>
            <p><strong>Date:</strong> ${new Date(order.created_at).toLocaleDateString()}</p>
            <p><strong>Total:</strong> &#8377;${order.total_amount.toFixed(2)}</p>
            <span class="order-status status-${order.status}">${order.status}</span>
            <p><strong>Shipping Address:</strong> ${escapeHtml(order.shipping_address)}</p>
            <h4>Items:</h4>
            <ul>
                ${order.items.map(item => `
                    <li>${escapeHtml(item.book.title)} - Qty: ${item.quantity} - &#8377;${item.price.toFixed(2)}</li>
                `).join('')}
            </ul>
        </div>
    `).join('');
}

async function viewBookDetail(bookId) {
    try {
        const [bookRes, reviewsRes, ratingRes] = await Promise.all([
            fetch(`${API_URL}/books/${bookId}`),
            fetch(`${API_URL}/reviews/book/${bookId}`),
            fetch(`${API_URL}/reviews/book/${bookId}/average-rating`)
        ]);
        const book = await bookRes.json();
        const reviews = await reviewsRes.json();
        const rating = await ratingRes.json();

        document.getElementById('bookDetailContent').innerHTML = `
            <div class="book-detail">
                <button onclick="showSection('books')" class="btn-back">&#8592; Back to Books</button>
                <div class="book-detail-header">
                    ${bookImageHtml(book.image_url)}
                    <div class="book-detail-info">
                        <h2>${escapeHtml(book.title)}</h2>
                        <p class="author">by ${escapeHtml(book.author)}</p>
                        <div class="book-detail-tags">
                            <span class="category">${escapeHtml(book.category)}</span>
                            <span class="condition-badge">${escapeHtml(book.condition.replace('_', ' '))}</span>
                            ${book.isbn ? `<span class="isbn-badge">ISBN: ${escapeHtml(book.isbn)}</span>` : ''}
                        </div>
                    </div>
                    <div class="book-detail-price-box">
                        <p class="price">&#8377;${book.price.toFixed(2)}</p>
                        <button onclick="addToCart(${book.id})" class="btn-add-cart btn-large">&#128722; Add to Cart</button>
                        <p class="seller-info">Sold by <strong>${escapeHtml(book.seller?.full_name || 'Unknown')}</strong></p>
                    </div>
                </div>
                <div class="book-detail-body">
                    <h3>Description</h3>
                    <p class="description">${escapeHtml(book.description || 'No description available.')}</p>
                </div>
                <div class="rating-summary">
                    <span class="rating-stars">&#11088; ${rating.average_rating.toFixed(1)} / 5.0</span>
                    <span class="rating-count">(${rating.total_reviews} review${rating.total_reviews !== 1 ? 's' : ''})</span>
                </div>
                <div class="reviews-section">
                    <h3>Reviews</h3>
                    ${getToken() ? `
                        <div class="add-review">
                            <h4>Write a Review</h4>
                            <form onsubmit="addReview(event, ${book.id})">
                                <select name="rating" required>
                                    <option value="">Select Rating</option>
                                    <option value="5">5 - Excellent</option>
                                    <option value="4">4 - Good</option>
                                    <option value="3">3 - Average</option>
                                    <option value="2">2 - Below Average</option>
                                    <option value="1">1 - Poor</option>
                                </select>
                                <textarea name="comment" placeholder="Share your thoughts..." rows="3"></textarea>
                                <button type="submit" class="btn-primary">Submit Review</button>
                            </form>
                        </div>` : '<p>Please login to write a review.</p>'}
                    <div class="reviews-list">
                        ${reviews.length > 0 ? reviews.map(review => `
                            <div class="review-card">
                                <div class="review-header">
                                    <strong>${escapeHtml(review.user?.full_name || 'Anonymous')}</strong>
                                    <span class="review-rating">${'&#11088;'.repeat(review.rating)}</span>
                                </div>
                                <p>${escapeHtml(review.comment || '')}</p>
                                <small>${new Date(review.created_at).toLocaleDateString()}</small>
                            </div>`).join('') : '<p>No reviews yet. Be the first to review!</p>'}
                    </div>
                </div>
            </div>`;
        showSection('bookDetail');
    } catch (e) {
        showAlert('Failed to load book details', 'error');
    }
}

async function addReview(event, bookId) {
    event.preventDefault();
    const formData = new FormData(event.target);
    try {
        const response = await authFetch(`${API_URL}/reviews`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                book_id: bookId,
                rating: parseInt(formData.get('rating')),
                comment: formData.get('comment')
            })
        });
        if (response && response.ok) {
            showAlert('Review added successfully!', 'success');
            viewBookDetail(bookId);
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Failed to add review', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

async function loadProfile() {
    if (!getToken()) {
        document.getElementById('profileContent').innerHTML = '<p>Please login to view profile.</p>';
        return;
    }
    document.getElementById('profileContent').innerHTML = '<p>Loading profile...</p>';
    try {
        const response = await authFetch(`${API_URL}/auth/me`);
        if (response && response.ok) {
            currentUser = await response.json();
            displayProfile(currentUser);
            return;
        }
    } catch (e) {}
    try {
        const payload = JSON.parse(atob(getToken().split('.')[1]));
        currentUser = { full_name: payload.sub, username: payload.sub, email: '-', phone: '', address: '', is_admin: false, created_at: new Date().toISOString() };
        displayProfile(currentUser);
    } catch (_) {
        showAlert('Failed to load profile', 'error');
    }
}

function displayProfile(user) {
    const memberSince = new Date(user.created_at).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById('profileContent').innerHTML = `
        <div class="profile-card" id="profileView">
            <div class="profile-avatar">
                <span class="avatar-icon">&#128100;</span>
                <h3>${escapeHtml(user.full_name)}</h3>
                <span class="username-tag">@${escapeHtml(user.username)}</span>
                ${user.is_admin ? '<span class="admin-badge">Admin</span>' : ''}
            </div>
            <div class="profile-details">
                <div class="profile-field"><label>Email</label><span>${escapeHtml(user.email)}</span></div>
                <div class="profile-field"><label>Username</label><span>${escapeHtml(user.username)}</span></div>
                <div class="profile-field"><label>Phone</label><span>${user.phone ? escapeHtml(user.phone) : '<em>Not provided</em>'}</span></div>
                <div class="profile-field"><label>Address</label><span>${user.address ? escapeHtml(user.address) : '<em>Not provided</em>'}</span></div>
                <div class="profile-field"><label>Member Since</label><span>${memberSince}</span></div>
            </div>
            <button onclick="showEditProfile()" class="btn-primary" style="margin-top:1.5rem;">Edit Profile</button>
        </div>
        <div class="profile-edit" id="profileEdit" style="display:none;">
            <h3>Edit Profile</h3>
            <form onsubmit="handleProfileUpdate(event)">
                <label>Full Name *</label>
                <input type="text" name="full_name" value="${escapeHtml(user.full_name)}" required>
                <label>Email *</label>
                <input type="email" name="email" value="${escapeHtml(user.email)}" required>
                <label>Phone</label>
                <input type="tel" name="phone" value="${escapeHtml(user.phone || '')}">
                <label>Address</label>
                <textarea name="address" rows="3">${escapeHtml(user.address || '')}</textarea>
                <div class="form-actions">
                    <button type="button" onclick="cancelEditProfile()" class="btn-cancel">Cancel</button>
                    <button type="submit" class="btn-primary">Save Changes</button>
                </div>
            </form>
        </div>`;
}

function showEditProfile() {
    document.getElementById('profileView').style.display = 'none';
    document.getElementById('profileEdit').style.display = 'block';
}

function cancelEditProfile() {
    document.getElementById('profileView').style.display = 'block';
    document.getElementById('profileEdit').style.display = 'none';
}

async function handleProfileUpdate(event) {
    event.preventDefault();
    const data = {};
    new FormData(event.target).forEach((value, key) => { if (value.trim()) data[key] = value.trim(); });
    try {
        const response = await authFetch(`${API_URL}/auth/me`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (response && response.ok) {
            currentUser = await response.json();
            document.getElementById('userName').textContent = currentUser.full_name || currentUser.username;
            showAlert('Profile updated successfully!', 'success');
            displayProfile(currentUser);
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Failed to update profile', 'error');
        }
    } catch (e) {
        showAlert('Network error. Please try again.', 'error');
    }
}

// ─── Map Location Picker ─────────────────────────────────────────────────────
let mapInstance = null;
let mapMarker = null;

function openMapPicker() {
    const overlay = document.createElement('div');
    overlay.id = 'mapOverlay';
    overlay.innerHTML = `
        <div class="map-modal">
            <div class="map-modal-header">
                <span>📍 Pick Delivery Location</span>
                <button onclick="document.getElementById('mapOverlay').remove()" class="map-close">✕</button>
            </div>
            <div class="map-search-bar">
                <input type="text" id="mapSearchInput" placeholder="Search area, city, pincode..." class="map-search-input">
                <button onclick="searchMapLocation()" class="map-search-btn">Search</button>
                <button onclick="useMyLocation()" class="map-locate-btn">📍 My Location</button>
            </div>
            <div id="mapContainer" style="height:380px;width:100%;"></div>
            <div id="mapSelectedAddress" class="map-address-preview">Click on map to select location</div>
            <button onclick="confirmMapLocation()" class="map-confirm-btn">✅ Confirm This Location</button>
        </div>`;
    document.body.appendChild(overlay);

    setTimeout(() => {
        mapInstance = L.map('mapContainer').setView([20.5937, 78.9629], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap'
        }).addTo(mapInstance);

        mapInstance.on('click', async (e) => {
            const { lat, lng } = e.latlng;
            if (mapMarker) mapMarker.remove();
            mapMarker = L.marker([lat, lng]).addTo(mapInstance);
            document.getElementById('mapSelectedAddress').textContent = 'Fetching address...';
            const addr = await reverseGeocode(lat, lng);
            document.getElementById('mapSelectedAddress').textContent = addr;
            mapMarker._address = addr;
        });

        document.getElementById('mapSearchInput').addEventListener('keydown', e => {
            if (e.key === 'Enter') { e.preventDefault(); searchMapLocation(); }
        });
    }, 100);
}

async function reverseGeocode(lat, lng) {
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`);
        const data = await res.json();
        return data.display_name || `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    } catch {
        return `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    }
}

async function searchMapLocation() {
    const query = document.getElementById('mapSearchInput').value.trim();
    if (!query) return;
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=1`);
        const data = await res.json();
        if (!data.length) { alert('Location not found. Try a different search.'); return; }
        const { lat, lon, display_name } = data[0];
        mapInstance.setView([lat, lon], 15);
        if (mapMarker) mapMarker.remove();
        mapMarker = L.marker([lat, lon]).addTo(mapInstance);
        mapMarker._address = display_name;
        document.getElementById('mapSelectedAddress').textContent = display_name;
    } catch {
        alert('Search failed. Please try again.');
    }
}

function useMyLocation() {
    if (!navigator.geolocation) { alert('Geolocation not supported by your browser.'); return; }
    navigator.geolocation.getCurrentPosition(async (pos) => {
        const { latitude: lat, longitude: lng } = pos.coords;
        mapInstance.setView([lat, lng], 16);
        if (mapMarker) mapMarker.remove();
        mapMarker = L.marker([lat, lng]).addTo(mapInstance);
        document.getElementById('mapSelectedAddress').textContent = 'Fetching address...';
        const addr = await reverseGeocode(lat, lng);
        document.getElementById('mapSelectedAddress').textContent = addr;
        mapMarker._address = addr;
    }, () => alert('Could not get your location. Please allow location access.'));
}

function confirmMapLocation() {
    if (!mapMarker || !mapMarker._address) {
        alert('Please click on the map to select a location first.');
        return;
    }
    document.getElementById('shippingAddressInput').value = mapMarker._address;
    document.getElementById('mapOverlay').remove();
    mapInstance = null;
    mapMarker = null;
}



async function loadDashboard() {
    if (!currentUser || !currentUser.is_admin) {
        showAlert('Admin access required', 'error');
        showSection('home');
        return;
    }
    try {
        const [statsRes, usersRes, ordersRes] = await Promise.all([
            authFetch(`${API_URL}/admin/stats`),
            authFetch(`${API_URL}/admin/users`),
            authFetch(`${API_URL}/admin/orders`)
        ]);
        const stats = await statsRes.json();
        const users = await usersRes.json();
        const orders = await ordersRes.json();

        document.getElementById('statUsers').textContent = stats.total_users;
        document.getElementById('statBooks').textContent = stats.total_books;
        document.getElementById('statAvailable').textContent = stats.available_books;
        document.getElementById('statOrders').textContent = stats.total_orders;

        renderAdminUsers(users);
        renderAdminOrders(orders);
    } catch (e) {
        showAlert('Failed to load dashboard', 'error');
    }
}

function renderAdminUsers(users) {
    const div = document.getElementById('adminUsersList');
    if (!users.length) { div.innerHTML = '<p>No users found.</p>'; return; }
    div.innerHTML = `
        <table class="admin-table">
            <thead><tr><th>ID</th><th>Name</th><th>Username</th><th>Email</th><th>Role</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
                ${users.map(u => `
                <tr>
                    <td>${u.id}</td>
                    <td>${escapeHtml(u.full_name)}</td>
                    <td>@${escapeHtml(u.username)}</td>
                    <td>${escapeHtml(u.email)}</td>
                    <td>${u.is_admin ? '<span class="admin-badge">Admin</span>' : 'User'}</td>
                    <td><span class="status-pill ${u.is_active ? 'active' : 'inactive'}">${u.is_active ? 'Active' : 'Inactive'}</span></td>
                    <td>${!u.is_admin ? `<button onclick="toggleUser(${u.id})" class="btn-sm">${u.is_active ? 'Deactivate' : 'Activate'}</button>` : '—'}</td>
                </tr>`).join('')}
            </tbody>
        </table>`;
}

function renderAdminOrders(orders) {
    const div = document.getElementById('adminOrdersList');
    if (!orders.length) { div.innerHTML = '<p>No orders found.</p>'; return; }
    div.innerHTML = `
        <table class="admin-table">
            <thead><tr><th>ID</th><th>Buyer</th><th>Amount</th><th>Payment</th><th>Status</th><th>Date</th><th>Update</th></tr></thead>
            <tbody>
                ${orders.map(o => `
                <tr>
                    <td>#${o.id}</td>
                    <td>${o.buyer_id}</td>
                    <td>₹${o.total_amount.toFixed(2)}</td>
                    <td>${escapeHtml(o.payment_method || '—')}</td>
                    <td><span class="order-status status-${o.status}">${o.status}</span></td>
                    <td>${new Date(o.created_at).toLocaleDateString()}</td>
                    <td>
                        <select onchange="updateOrderStatus(${o.id}, this.value)" class="status-select">
                            ${['pending','confirmed','shipped','delivered','cancelled'].map(s =>
                                `<option value="${s}" ${o.status === s ? 'selected' : ''}>${s}</option>`
                            ).join('')}
                        </select>
                    </td>
                </tr>`).join('')}
            </tbody>
        </table>`;
}

async function toggleUser(userId) {
    const res = await authFetch(`${API_URL}/admin/users/${userId}/toggle-active`, { method: 'PUT' });
    if (res && res.ok) { showAlert('User status updated', 'success'); loadDashboard(); }
    else showAlert('Failed to update user', 'error');
}

async function updateOrderStatus(orderId, newStatus) {
    const res = await authFetch(`${API_URL}/admin/orders/${orderId}/status?status=${newStatus}`, { method: 'PUT' });
    if (res && res.ok) showAlert('Order status updated', 'success');
    else showAlert('Failed to update order', 'error');
}

function switchTab(tabId, btn) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    btn.classList.add('active');
}

// ─── Wishlist ─────────────────────────────────────────────────────────────────
async function toggleWishlist(bookId, btn) {
    if (!getToken()) { showAlert('Please login to use wishlist', 'error'); return; }
    try {
        const res = await authFetch(`${API_URL}/wishlist/${bookId}`, { method: 'POST' });
        if (res && res.ok) {
            btn.textContent = '❤️';
            showAlert('Added to wishlist!', 'success');
        } else {
            // Already in wishlist — remove it
            await authFetch(`${API_URL}/wishlist/${bookId}`, { method: 'DELETE' });
            showAlert('Removed from wishlist', 'info');
        }
    } catch (e) { showAlert('Error updating wishlist', 'error'); }
}

async function loadWishlist() {
    if (!getToken()) { showSection('login'); return; }
    const res = await authFetch(`${API_URL}/wishlist`);
    if (!res || !res.ok) { showAlert('Failed to load wishlist', 'error'); return; }
    const items = await res.json();
    const grid = document.getElementById('wishlistGrid');
    if (!items.length) {
        grid.innerHTML = '<p>Your wishlist is empty. Browse books and click ❤️ to save them!</p>';
        return;
    }
    grid.innerHTML = items.map(item => `
        <div class="book-card" onclick="viewBookDetail(${item.book.id})" style="cursor:pointer;">
            ${bookImageHtml(item.book.image_url)}
            <div class="book-card-body">
                <h3>${escapeHtml(item.book.title)}</h3>
                <p class="author">by ${escapeHtml(item.book.author)}</p>
                <div class="book-card-meta">
                    <span class="category">${escapeHtml(item.book.category)}</span>
                    <span class="condition-badge">${escapeHtml(item.book.condition.replace('_',' '))}</span>
                </div>
            </div>
            <div class="book-card-footer">
                <p class="price">&#8377;${item.book.price.toFixed(2)}</p>
                <div style="display:flex;gap:0.4rem;">
                    <button onclick="event.stopPropagation(); removeWishlist(${item.book.id})" class="btn-wishlist" title="Remove">🗑️</button>
                    <button onclick="event.stopPropagation(); addToCart(${item.book.id})" class="btn-add-cart">🛒 Cart</button>
                </div>
            </div>
        </div>`).join('');
}

async function removeWishlist(bookId) {
    await authFetch(`${API_URL}/wishlist/${bookId}`, { method: 'DELETE' });
    showAlert('Removed from wishlist', 'info');
    loadWishlist();
}

// ─── Book Swap ────────────────────────────────────────────────────────────────
async function loadSwapBooks() {
    const res = await fetch(`${API_URL}/books`);
    const books = await res.json();
    const swappable = books.filter(b => b.swap_available);
    const grid = document.getElementById('swapBooksGrid');
    if (!swappable.length) {
        grid.innerHTML = '<p>No books available for swap yet. List your book with "Available for Swap" checked!</p>';
        return;
    }
    grid.innerHTML = swappable.map(book => `
        <div class="book-card" onclick="viewBookDetail(${book.id})" style="cursor:pointer;">
            ${bookImageHtml(book.image_url)}
            <div class="book-card-body">
                <h3>${escapeHtml(book.title)}</h3>
                <p class="author">by ${escapeHtml(book.author)}</p>
                <div class="book-card-meta">
                    <span class="category">${escapeHtml(book.category)}</span>
                    <span class="swap-badge">🔄 Swap</span>
                </div>
            </div>
            <div class="book-card-footer">
                <p class="price">&#8377;${book.price.toFixed(2)}</p>
                <button onclick="event.stopPropagation(); openSwapModal(${book.id}, '${escapeHtml(book.title)}')" class="btn-swap">🔄 Offer Swap</button>
            </div>
        </div>`).join('');
}

async function openSwapModal(wantedBookId, wantedTitle) {
    if (!getToken()) { showAlert('Please login to swap books', 'error'); return; }
    const res = await authFetch(`${API_URL}/books/seller/my-books`);
    const myBooks = await res.json();
    const available = myBooks.filter(b => b.is_available);
    if (!available.length) {
        showAlert('You need to list at least one book to offer a swap!', 'error');
        return;
    }
    const overlay = document.createElement('div');
    overlay.id = 'swapModalOverlay';
    overlay.innerHTML = `
        <div class="payment-modal">
            <div class="payment-header">🔄 Offer Swap for "${escapeHtml(wantedTitle)}"
                <button onclick="document.getElementById('swapModalOverlay').remove()" style="background:transparent;border:none;color:#fff;font-size:1.2rem;cursor:pointer;float:right;">✕</button>
            </div>
            <div style="padding:1.5rem;">
                <label style="font-weight:600;display:block;margin-bottom:0.5rem;">Select your book to offer:</label>
                <select id="swapOfferedBook" class="pay-input">
                    ${available.map(b => `<option value="${b.id}">${escapeHtml(b.title)} — ₹${b.price}</option>`).join('')}
                </select>
                <label style="font-weight:600;display:block;margin:0.75rem 0 0.5rem;">Message (optional):</label>
                <textarea id="swapMessage" class="pay-input" rows="2" placeholder="Why do you want to swap?"></textarea>
                <button class="pay-btn" onclick="submitSwap(${wantedBookId})">Send Swap Offer</button>
                <button class="pay-cancel" onclick="document.getElementById('swapModalOverlay').remove()">Cancel</button>
            </div>
        </div>`;
    document.body.appendChild(overlay);
}

async function submitSwap(wantedBookId) {
    const offeredBookId = parseInt(document.getElementById('swapOfferedBook').value);
    const message = document.getElementById('swapMessage').value;
    const res = await authFetch(`${API_URL}/swap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wanted_book_id: wantedBookId, offered_book_id: offeredBookId, message })
    });
    document.getElementById('swapModalOverlay').remove();
    if (res && res.ok) {
        showAlert('Swap offer sent! The owner will review your offer.', 'success');
    } else {
        const err = await res.json();
        showAlert(err.detail || 'Failed to send swap offer', 'error');
    }
}

async function loadSwapSent() {
    const res = await authFetch(`${API_URL}/swap/my-offers`);
    const offers = await res.json();
    const div = document.getElementById('swapSentList');
    if (!offers.length) { div.innerHTML = '<p>No swap offers sent yet.</p>'; return; }
    div.innerHTML = offers.map(o => `
        <div class="swap-offer-card">
            <div class="swap-offer-books">
                <div class="swap-book"><span>You want</span><strong>${escapeHtml(o.wanted_book.title)}</strong></div>
                <div class="swap-arrow">⇄</div>
                <div class="swap-book"><span>You offer</span><strong>${escapeHtml(o.offered_book.title)}</strong></div>
            </div>
            ${o.message ? `<p class="swap-msg">"${escapeHtml(o.message)}"</p>` : ''}
            <span class="swap-status status-${o.status}">${o.status}</span>
        </div>`).join('');
}

async function loadSwapReceived() {
    const res = await authFetch(`${API_URL}/swap/received`);
    const offers = await res.json();
    const div = document.getElementById('swapReceivedList');
    if (!offers.length) { div.innerHTML = '<p>No swap offers received yet.</p>'; return; }
    div.innerHTML = offers.map(o => `
        <div class="swap-offer-card">
            <p><strong>${escapeHtml(o.requester.full_name)}</strong> wants to swap:</p>
            <div class="swap-offer-books">
                <div class="swap-book"><span>They want</span><strong>${escapeHtml(o.wanted_book.title)}</strong></div>
                <div class="swap-arrow">⇄</div>
                <div class="swap-book"><span>They offer</span><strong>${escapeHtml(o.offered_book.title)}</strong></div>
            </div>
            ${o.message ? `<p class="swap-msg">"${escapeHtml(o.message)}"</p>` : ''}
            ${o.status === 'pending' ? `
                <div style="display:flex;gap:0.5rem;margin-top:0.75rem;">
                    <button onclick="respondSwap(${o.id},'accept')" class="btn-primary" style="flex:1;">✅ Accept</button>
                    <button onclick="respondSwap(${o.id},'reject')" class="btn-danger" style="flex:1;">❌ Reject</button>
                </div>` : `<span class="swap-status status-${o.status}">${o.status}</span>`}
        </div>`).join('');
}

async function respondSwap(offerId, action) {
    const res = await authFetch(`${API_URL}/swap/${offerId}/${action}`, { method: 'PUT' });
    if (res && res.ok) {
        const data = await res.json();
        showAlert(data.message, 'success');
        loadSwapReceived();
        if (action === 'accept') await fetchCurrentUser();
    } else {
        showAlert('Failed to respond to swap', 'error');
    }
}

// ─── Leaderboard & Eco Points ─────────────────────────────────────────────────
async function loadLeaderboard() {
    const [lbRes, badgeRes] = await Promise.all([
        fetch(`${API_URL}/extras/leaderboard`),
        getToken() ? authFetch(`${API_URL}/extras/my-badges`) : Promise.resolve(null)
    ]);

    const leaders = await lbRes.json();
    const div = document.getElementById('leaderboardList');
    div.innerHTML = `
        <h3 style="margin-bottom:1rem;">🏆 Top Eco Contributors</h3>
        <div class="leaderboard-table">
            ${leaders.map(u => `
                <div class="lb-row ${u.rank <= 3 ? 'lb-top' : ''}">
                    <span class="lb-rank">${u.rank === 1 ? '🥇' : u.rank === 2 ? '🥈' : u.rank === 3 ? '🥉' : '#' + u.rank}</span>
                    <span class="lb-name">${escapeHtml(u.full_name)} <small>@${escapeHtml(u.username)}</small></span>
                    <span class="lb-pts">${u.eco_points} 🌱</span>
                </div>`).join('')}
            ${!leaders.length ? '<p style="padding:1rem;color:#666;">No eco points earned yet. Start buying and selling!</p>' : ''}
        </div>`;

    if (badgeRes && badgeRes.ok) {
        const data = await badgeRes.json();
        const statsDiv = document.getElementById('ecoMyStats');
        statsDiv.innerHTML = `
            <div class="eco-my-card">
                <div class="eco-pts-big">${data.eco_points} <span>🌱</span></div>
                <p>Your Eco Points</p>
                <div class="badges-row">
                    ${data.badges.length
                        ? data.badges.map(b => `<span class="badge-pill" title="${b.desc}">${b.icon} ${b.label}</span>`).join('')
                        : '<span style="color:#888;font-size:0.9rem;">No badges yet — start buying, selling & swapping!</span>'}
                </div>
            </div>`;
    }
}
