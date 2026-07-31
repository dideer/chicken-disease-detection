from functools import wraps

from flask import g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from config import SECRET_KEY, TOKEN_MAX_AGE_SECONDS


def _serializer():
    return URLSafeTimedSerializer(SECRET_KEY, salt='poultry-disease-auth')


def generate_auth_token(user):
    return _serializer().dumps({
        'user_id': user['id'],
        'role': user['role'],
        'username': user['username']
    })


def decode_auth_token(token):
    try:
        return _serializer().loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        return None


def _extract_token():
    header = request.headers.get('Authorization', '').strip()
    if not header.startswith('Bearer '):
        return None
    return header.split(' ', 1)[1].strip()


def require_auth(admin_only=False):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            token = _extract_token()
            if not token:
                return jsonify({
                    'success': False,
                    'message': 'Authentication required.'
                }), 401

            payload = decode_auth_token(token)
            if not payload or 'user_id' not in payload:
                return jsonify({
                    'success': False,
                    'message': 'Invalid or expired session.'
                }), 401

            from app.models.user import User

            user = User.get_user_by_id(payload['user_id'])
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User account not found.'
                }), 401

            if user['status'] != 'active':
                return jsonify({
                    'success': False,
                    'message': 'Your account is inactive.'
                }), 403

            if admin_only and user['role'] != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Admin access required.'
                }), 403

            g.current_user = user
            return view(*args, **kwargs)

        return wrapped

    return decorator
