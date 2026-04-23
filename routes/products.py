from flask import Blueprint, jsonify, request
from app import db
from models.models import Product, Category, User


def check_admin():
    """Check if the current user is an admin via X-User-ID header."""
    try:
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return False
        user = User.query.get(int(user_id))
        return user and user.is_admin
    except:
        return False

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_all_products():
    """Get all products with optional filtering and pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '')
        featured = request.args.get('featured', type=bool)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Base query
        query = Product.query.filter_by(is_active=True)
        
        # Apply filters
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(
                db.or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%'),
                    Product.brand.ilike(f'%{search}%')
                )
            )
        
        if featured:
            query = query.filter_by(is_featured=True)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # Order by creation date (newest first)
        query = query.order_by(Product.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        products = pagination.items
        
        return jsonify({
            'success': True,
            'products': [p.to_dict() for p in products],
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'message': 'Product not found'
            }), 404
        
        return jsonify({
            'success': True,
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@products_bp.route('/', methods=['POST'])
def create_product():
    """Create a new product (admin only)."""
    try:
        # Check if user is admin
        if not check_admin():
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        data = request.get_json()
        
        product = Product(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            original_price=data.get('original_price'),
            stock_quantity=data.get('stock_quantity', 0),
            category_id=data.get('category_id'),
            brand=data.get('brand'),
            model=data.get('model'),
            image_url=data.get('image_url'),
            images=data.get('images'),
            specifications=data.get('specifications'),
            is_featured=data.get('is_featured', False)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product (admin only)."""
    try:
        # Check if user is admin
        if not check_admin():
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'message': 'Product not found'
            }), 404
        
        data = request.get_json()
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'original_price' in data:
            product.original_price = data['original_price']
        if 'stock_quantity' in data:
            product.stock_quantity = data['stock_quantity']
        if 'category_id' in data:
            product.category_id = data['category_id']
        if 'brand' in data:
            product.brand = data['brand']
        if 'model' in data:
            product.model = data['model']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'images' in data:
            product.images = data['images']
        if 'specifications' in data:
            product.specifications = data['specifications']
        if 'is_featured' in data:
            product.is_featured = data['is_featured']
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product (admin only)."""
    try:
        # Check if user is admin
        if not check_admin():
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'message': 'Product not found'
            }), 404
        
        # Soft delete - just mark as inactive
        product.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@products_bp.route('/featured', methods=['GET'])
def get_featured_products():
    """Get featured products for homepage."""
    try:
        products = Product.query.filter_by(
            is_featured=True, 
            is_active=True
        ).limit(8).all()
        
        return jsonify({
            'success': True,
            'products': [p.to_dict() for p in products]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@products_bp.route('/latest', methods=['GET'])
def get_latest_products():
    """Get latest products."""
    try:
        products = Product.query.filter_by(
            is_active=True
        ).order_by(Product.created_at.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'products': [p.to_dict() for p in products]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500