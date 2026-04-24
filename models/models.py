from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model for customers and admins."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)  # Nullable for Google OAuth users
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Password reset fields
    reset_code = db.Column(db.String(6))
    reset_code_expiry = db.Column(db.DateTime)
    
    # Google OAuth fields
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), default='local')  # 'local' or 'google'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set the user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify the user password."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Category(db.Model):
    """Category model for product categorization."""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'product_count': len(self.products)
        }


class Product(db.Model):
    """Product model for electronics items."""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)  # For showing discounts
    stock_quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    images = db.Column(db.JSON)  # Multiple product images
    specifications = db.Column(db.JSON)  # Technical specifications
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def to_dict(self):
        """Convert product to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'stock_quantity': self.stock_quantity,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'brand': self.brand,
            'model': self.model,
            'image_url': self.image_url,
            'images': self.images,
            'specifications': self.specifications,
            'rating': self.rating,
            'review_count': self.review_count,
            'is_featured': self.is_featured,
            'discount': round(((self.original_price - self.price) / self.original_price * 100) if self.original_price and self.original_price > self.price else 0, 1)
        }


class Order(db.Model):
    """Order model for customer purchases."""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def to_dict(self):
        """Convert order to dictionary."""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'status': self.status,
            'total_amount': self.total_amount,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class OrderItem(db.Model):
    """Order item model for individual products in an order."""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Convert order item to dictionary."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal
        }