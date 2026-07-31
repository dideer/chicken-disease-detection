from flask import Blueprint, jsonify, request

from app import bcrypt
from app.models.user import User
from app.utils.auth import generate_auth_token, require_auth
from app.utils.helpers import check_password, get_message

auth_bp = Blueprint('auth', __name__)


def _serialize_user(user):
    return {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role'],
        'status': user['status'],
        'is_admin': user['role'] == 'admin',
        'created_at': str(user['created_at'])
    }


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    lang = data.get('lang', 'en')

    if not username or not email or not password:
        return jsonify({
            'success': False,
            'message': get_message('register_error', lang)
        }), 400

    if User.find_by_username(username) or User.find_by_email(email):
        return jsonify({
            'success': False,
            'message': get_message('register_exists', lang)
        }), 409

    role = 'admin' if username.lower() == 'admin' else 'user'
    user_id = User.create_user(username, email, password, role=role, status='active')
    if not user_id:
        return jsonify({
            'success': False,
            'message': get_message('register_error', lang)
        }), 500

    return jsonify({
        'success': True,
        'message': get_message('register_success', lang),
        'user_id': user_id
    }), 201


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    lang = data.get('lang', 'en')

    User.ensure_admin_role(username)
    user = User.find_by_username(username)
    if not user:
        return jsonify({
            'success': False,
            'message': get_message('login_invalid', lang)
        }), 401

    if user['status'] != 'active':
        return jsonify({
            'success': False,
            'message': 'Your account is inactive. Please contact an administrator.'
        }), 403

    if not check_password(bcrypt, user['password'], password):
        return jsonify({
            'success': False,
            'message': get_message('login_invalid', lang)
        }), 401

    return jsonify({
        'success': True,
        'message': get_message('login_success', lang),
        'token': generate_auth_token(user),
        'user': _serialize_user(user)
    }), 200


@auth_bp.route('/api/me', methods=['GET'])
@require_auth()
def me():
    from flask import g

    return jsonify({
        'success': True,
        'user': _serialize_user(g.current_user)
    }), 200
