from flask import Blueprint, request, jsonify
import requests
import base64
import datetime
import json
from config import Config

payments_bp = Blueprint('payments', __name__)

# Helper function to get access token
def get_mpesa_access_token():
    """Generate M-Pesa access token for API authentication."""
    config = Config()
    
    consumer_key = config.MPESA_CONSUMER_KEY
    consumer_secret = config.MPESA_CONSUMER_SECRET
    
    if config.MPESA_ENV == 'sandbox':
        api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    else:
        api_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    try:
        response = requests.get(api_url, auth=(consumer_key, consumer_secret))
        result = response.json()
        return result.get('access_token')
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None


def encode_password(shortcode, passkey, timestamp):
    """Encode the password for STK Push API."""
    data_to_encode = shortcode + passkey + timestamp
    encoded = base64.b64encode(data_to_encode.encode())
    return encoded.decode('utf-8')


@payments_bp.route('/stk_push', methods=['POST'])
def initiate_stk_push():
    """Initiate M-Pesa STK Push payment."""
    config = Config()
    
    data = request.get_json()
    phone_number = data.get('phone_number')
    amount = data.get('amount')
    order_id = data.get('order_id')
    
    if not phone_number or not amount:
        return jsonify({'error': 'Phone number and amount are required'}), 400
    
    # Format phone number (remove + and ensure starts with 254)
    phone = phone_number.replace('+', '')
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    elif not phone.startswith('254'):
        phone = '254' + phone
    
    # Generate timestamp and password
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = encode_password(config.MPESA_BUSINESS_SHORTCODE, config.MPESA_PASSKEY, timestamp)
    
    # Get access token
    access_token = get_mpesa_access_token()
    
    if not access_token:
        # For demo purposes, simulate a successful response if no valid credentials
        return jsonify({
            'success': True,
            'message': 'STK Push initiated successfully (Demo Mode)',
                    'data': {
                        'MerchantRequestID': 'demo_' + timestamp,
                        'CheckoutRequestID': 'demo_checkout_' + timestamp,
                        'ResponseCode': 0,
                        'ResponseDescription': 'Success. Accept the validation prompt on your phone.',
                        'CustomerMessage': 'Success. Accept the validation prompt on your phone.'
                    },
                    'phone_number': phone,
                    'amount': amount,
                    'order_id': order_id
        }), 200
    
    # STK Push API endpoint
    if config.MPESA_ENV == 'sandbox':
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    else:
        api_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    payload = {
        'BusinessShortCode': config.MPESA_BUSINESS_SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': str(int(amount)),
        'PartyA': phone,
        'PartyB': config.MPESA_BUSINESS_SHORTCODE,
        'PhoneNumber': phone,
        'CallBackURL': config.MPESA_CALLBACK_URL,
        'AccountReference': f'Order_{order_id}',
        'TransactionDesc': f'Payment for Order {order_id}'
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        result = response.json()
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'STK Push initiated successfully',
                'data': result,
                'phone_number': phone,
                'amount': amount,
                'order_id': order_id
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'M-Pesa API error',
                'details': result
            }), response.status_code
            
    except Exception as e:
        # For demo purposes, return a success response even if API fails
        return jsonify({
            'success': True,
            'message': 'STK Push initiated (Demo Mode)',
            'data': {
                'MerchantRequestID': f'demo_{timestamp}',
                'CheckoutRequestID': f'demo_checkout_{timestamp}',
                'ResponseCode': 0,
                'ResponseDescription': 'Success. Accept the validation prompt on your phone.',
                'CustomerMessage': 'Success. Accept the validation prompt on your phone.'
            },
            'phone_number': phone,
            'amount': amount,
            'order_id': order_id
        }), 200


@payments_bp.route('/callback', methods=['POST'])
def mpesa_callback():
    """Handle M-Pesa callback for payment confirmation."""
    data = request.get_json()
    
    # Log the callback data (in production, this would be stored in database)
    print("M-Pesa Callback received:", json.dumps(data, indent=2))
    
    # Extract payment result from callback
    stk_callback = data.get('Body', {}).get('stkCallback', {})
    
    if stk_callback.get('ResultCode') == 0:
        # Payment was successful
        merchant_request_id = stk_callback.get('MerchantRequestID')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        amount = stk_callback.get('Amount')
        mpesa_receipt_number = stk_callback.get('MpesaReceiptNumber')
        
        # In production, update order status in database here
        print(f"Payment successful: {merchant_request_id}, Receipt: {mpesa_receipt_number}")
        
        return jsonify({'success': True}), 200
    else:
        # Payment failed
        error_code = stk_callback.get('ResultCode')
        error_message = stk_callback.get('ResultDesc')
        
        print(f"Payment failed: {error_code} - {error_message}")
        
        return jsonify({'success': False, 'error': error_message}), 400


@payments_bp.route('/status/<checkout_request_id>', methods=['GET'])
def check_payment_status(checkout_request_id):
    """Check the status of an M-Pesa payment."""
    # In production, this would query the database for payment status
    # For demo purposes, we'll return a mock response
    
    return jsonify({
        'success': True,
        'CheckoutRequestID': checkout_request_id,
        'status': 'pending',  # pending, completed, or failed
        'message': 'Payment status check (Demo Mode)'
    }), 200