from flask import Blueprint, jsonify, request
from app import db
from models.models import Order, OrderItem, Product
from datetime import datetime
import uuid

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
def get_all_orders():
    """Get all orders (admin) or user orders."""
    try:
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')
        
        query = Order.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        orders = query.order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'orders': [o.to_dict() for o in orders]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a single order by ID."""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@orders_bp.route('/', methods=['POST'])
def create_order():
    """Create a new order."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'items', 'shipping_address', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Validate items
        if not data['items'] or len(data['items']) == 0:
            return jsonify({
                'success': False,
                'message': 'Order must have at least one item'
            }), 400
        
        # Generate unique order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        # Calculate total and create order items
        total_amount = 0
        order_items = []
        
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({
                    'success': False,
                    'message': f'Product {item["product_id"]} not found'
                }), 404
            
            if product.stock_quantity < item['quantity']:
                return jsonify({
                    'success': False,
                    'message': f'Insufficient stock for {product.name}'
                }), 400
            
            subtotal = product.price * item['quantity']
            total_amount += subtotal
            
            order_items.append(OrderItem(
                product_id=product.id,
                quantity=item['quantity'],
                unit_price=product.price,
                subtotal=subtotal
            ))
            
            # Reduce stock
            product.stock_quantity -= item['quantity']
        
        # Create order
        order = Order(
            order_number=order_number,
            user_id=data['user_id'],
            total_amount=total_amount,
            shipping_address=data['shipping_address'],
            payment_method=data['payment_method'],
            notes=data.get('notes', '')
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order items
        for item in order_items:
            item.order_id = order.id
            db.session.add(item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status (admin only)."""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        data = request.get_json()
        
        if 'status' in data:
            order.status = data['status']
        if 'payment_status' in data:
            order.payment_status = data['payment_status']
        if 'notes' in data:
            order.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """Cancel an order."""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        if order.status not in ['pending', 'processing']:
            return jsonify({
                'success': False,
                'message': 'Cannot cancel order in current status'
            }), 400
        
        # Restore stock
        for item in order.items:
            product = item.product
            if product:
                product.stock_quantity += item.quantity
        
        order.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@orders_bp.route('/track/<order_number>', methods=['GET'])
def track_order(order_number):
    """Track order by order number."""
    try:
        order = Order.query.filter_by(order_number=order_number).first()
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500