from flask import Blueprint, jsonify, request
from app import db
from models.models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    """Get all product categories."""
    try:
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'categories': [c.to_dict() for c in categories]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a single category by ID."""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({
                'success': False,
                'message': 'Category not found'
            }), 404
        
        return jsonify({
            'success': True,
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@categories_bp.route('/', methods=['POST'])
def create_category():
    """Create a new category (admin only)."""
    try:
        data = request.get_json()
        
        category = Category(
            name=data.get('name'),
            description=data.get('description'),
            image_url=data.get('image_url')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update a category (admin only)."""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({
                'success': False,
                'message': 'Category not found'
            }), 404
        
        data = request.get_json()
        
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'image_url' in data:
            category.image_url = data['image_url']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category (admin only)."""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({
                'success': False,
                'message': 'Category not found'
            }), 404
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500