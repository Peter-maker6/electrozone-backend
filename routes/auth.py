from flask import Blueprint, request, jsonify
from flask_mail import Message
from app import db, mail
from models.models import User
from datetime import datetime, timedelta
import random
import string
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from config import Config

auth_bp = Blueprint('auth', __name__)

def generate_reset_code(length=6):
    """Generate a random numeric reset code."""
    return ''.join(random.choices(string.digits, k=length))

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset code to user's email."""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Don't reveal that the email doesn't exist for security
        return jsonify({'message': 'If the email exists, a reset code has been sent'}), 200
    
    # Generate reset code
    reset_code = generate_reset_code()
    user.reset_code = reset_code
    user.reset_code_expiry = datetime.utcnow() + timedelta(minutes=15)  # Code expires in 15 minutes
    
    db.session.commit()
    
    # Send email with reset code
    try:
        msg = Message(
            'Password Reset Code - D&J Electronics and Electricals',
            sender=Config.MAIL_DEFAULT_SENDER,
            recipients=[email]
        )
        msg.body = f'''
Hello {user.full_name},

You requested a password reset for your account.

Your reset code is: {reset_code}

This code will expire in 15 minutes.

If you didn't request this, please ignore this email.

Best regards,
D&J Electronics and Electricals Team
'''
        mail.send(msg)
    except Exception as e:
        # Log the error but don't reveal to user
        print(f"Email sending failed: {str(e)}")
    
    return jsonify({'message': 'If the email exists, a reset code has been sent'}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Verify reset code and set new password."""
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('new_password')
    
    if not all([email, code, new_password]):
        return jsonify({'error': 'Email, code, and new password are required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'Invalid email or code'}), 400
    
    # Check if code is valid and not expired
    if user.reset_code != code:
        return jsonify({'error': 'Invalid reset code'}), 400
    
    if not user.reset_code_expiry or user.reset_code_expiry < datetime.utcnow():
        return jsonify({'error': 'Reset code has expired'}), 400
    
    # Update password
    user.set_password(new_password)
    user.reset_code = None
    user.reset_code_expiry = None
    db.session.commit()
    
    return jsonify({'message': 'Password has been reset successfully'}), 200

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    """Authenticate user with Google OAuth."""
    data = request.get_json()
    token = data.get('token')  # Google ID token from frontend
    
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    try:
        # Verify the Google token
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), Config.GOOGLE_CLIENT_ID
        )
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return jsonify({'error': 'Invalid token issuer'}), 400
        
        google_id = idinfo['sub']
        email = idinfo['email']
        full_name = idinfo.get('name', '')
        
        # Check if user exists
        user = User.query.filter_by(google_id=google_id).first()
        
        if not user:
            # Check if email already exists with local auth
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                # Link Google account to existing user
                existing_user.google_id = google_id
                existing_user.auth_provider = 'google'
                user = existing_user
            else:
                # Create new user
                username = email.split('@')[0] + '_' + ''.join(random.choices(string.digits, k=4))
                user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    google_id=google_id,
                    auth_provider='google'
                )
                db.session.add(user)
            
        db.session.commit()
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid token: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Authentication failed: {str(e)}'}), 400

@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback (for web-based flow)."""
    return jsonify({'message': 'Use the POST /api/auth/google endpoint with ID token instead'}), 200
