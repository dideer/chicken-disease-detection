from flask import Blueprint, g, jsonify, request

from app.models.detection import Detection
from app.models.user import User
from app.utils.auth import require_auth

admin_bp = Blueprint('admin', __name__)


def _clean_user_payload(data, require_password):
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    role = (data.get('role') or 'user').strip().lower()
    status = (data.get('status') or 'active').strip().lower()
    password = data.get('password') or ''

    if not username or not email:
        return None, 'Username and email are required.'
    if role not in User.VALID_ROLES:
        return None, 'Role must be admin or user.'
    if status not in User.VALID_STATUSES:
        return None, 'Status must be active or inactive.'
    if require_password and not password:
        return None, 'Password is required.'

    return {
        'username': username,
        'email': email,
        'role': role,
        'status': status,
        'password': password
    }, None


def _serialize_user(user):
    return {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role'],
        'status': user['status'],
        'created_at': str(user['created_at'])
    }


@admin_bp.route('/api/admin/summary', methods=['GET'])
@require_auth(admin_only=True)
def admin_summary():
    detection_summary = Detection.get_admin_summary()
    return jsonify({
        'success': True,
        'summary': {
            'total_users': User.get_total_users(),
            **detection_summary
        }
    }), 200


@admin_bp.route('/api/admin/users', methods=['GET'])
@require_auth(admin_only=True)
def list_users():
    search = request.args.get('search', '').strip()
    role = request.args.get('role', '').strip().lower()
    status = request.args.get('status', '').strip().lower()
    users = User.get_all_users(search=search, role=role, status=status)
    return jsonify({
        'success': True,
        'users': [{
            **user,
            'created_at': str(user['created_at'])
        } for user in users],
        'total': len(users)
    }), 200


@admin_bp.route('/api/admin/users', methods=['POST'])
@require_auth(admin_only=True)
def create_user():
    payload, error = _clean_user_payload(request.get_json() or {}, require_password=True)
    if error:
        return jsonify({'success': False, 'message': error}), 400

    if User.find_by_username(payload['username']):
        return jsonify({'success': False, 'message': 'Username already exists.'}), 409
    if User.find_by_email(payload['email']):
        return jsonify({'success': False, 'message': 'Email already exists.'}), 409

    user_id = User.create_user(
        payload['username'],
        payload['email'],
        payload['password'],
        payload['role'],
        payload['status']
    )
    if not user_id:
        return jsonify({'success': False, 'message': 'Failed to create user.'}), 500

    created_user = User.get_user_by_id(user_id)

    return jsonify({
        'success': True,
        'message': 'User created successfully.',
        'user': _serialize_user(created_user)
    }), 201


@admin_bp.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@require_auth(admin_only=True)
def update_user(user_id):
    existing = User.get_user_by_id(user_id)
    if not existing:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    payload, error = _clean_user_payload(request.get_json() or {}, require_password=False)
    if error:
        return jsonify({'success': False, 'message': error}), 400

    other_user = User.find_by_username(payload['username'])
    if other_user and other_user['id'] != user_id:
        return jsonify({'success': False, 'message': 'Username already exists.'}), 409

    other_email = User.find_by_email(payload['email'])
    if other_email and other_email['id'] != user_id:
        return jsonify({'success': False, 'message': 'Email already exists.'}), 409

    if g.current_user['id'] == user_id and payload['role'] != 'admin':
        return jsonify({'success': False, 'message': 'You cannot remove your own admin role.'}), 400

    if g.current_user['id'] == user_id and payload['status'] != 'active':
        return jsonify({'success': False, 'message': 'You cannot deactivate your own account.'}), 400

    updated = User.update_user(
        user_id,
        payload['username'],
        payload['email'],
        payload['role'],
        payload['status'],
        payload['password'] or None
    )
    if not updated:
        return jsonify({'success': False, 'message': 'Failed to update user.'}), 500

    refreshed = User.get_user_by_id(user_id)
    return jsonify({
        'success': True,
        'message': 'User updated successfully.',
        'user': _serialize_user(refreshed)
    }), 200


@admin_bp.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@require_auth(admin_only=True)
def delete_user(user_id):
    if g.current_user['id'] == user_id:
        return jsonify({'success': False, 'message': 'You cannot delete your own account.'}), 400

    if not User.get_user_by_id(user_id):
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    deleted = User.delete_user(user_id)
    if not deleted:
        return jsonify({'success': False, 'message': 'Failed to delete user.'}), 500

    return jsonify({
        'success': True,
        'message': 'User deleted successfully.'
    }), 200


@admin_bp.route('/api/admin/users/<int:user_id>/status', methods=['PATCH'])
@require_auth(admin_only=True)
def update_user_status(user_id):
    data = request.get_json() or {}
    status = (data.get('status') or '').strip().lower()

    if status not in User.VALID_STATUSES:
        return jsonify({'success': False, 'message': 'Status must be active or inactive.'}), 400

    if g.current_user['id'] == user_id and status != 'active':
        return jsonify({'success': False, 'message': 'You cannot deactivate your own account.'}), 400

    if not User.get_user_by_id(user_id):
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    updated = User.set_status(user_id, status)
    if not updated:
        return jsonify({'success': False, 'message': 'Failed to update user status.'}), 500

    return jsonify({
        'success': True,
        'message': f'User status updated to {status}.'
    }), 200


@admin_bp.route('/api/admin/detections', methods=['GET'])
@require_auth(admin_only=True)
def list_detections():
    result_filter = request.args.get('result', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    detections = Detection.get_all_detections(
        result_filter=result_filter,
        date_from=date_from,
        date_to=date_to
    )

    search = request.args.get('search', '').strip().lower()
    if search:
        detections = [
            item for item in detections
            if search in (item['username'] or '').lower()
            or search in (item['predicted_class'] or '').lower()
        ]

    return jsonify({
        'success': True,
        'detections': [{
            **item,
            'detected_at': str(item['detected_at']),
            'image_url': f"/uploads/{item['image_name']}" if item['image_name'] else ''
        } for item in detections],
        'total': len(detections)
    }), 200


@admin_bp.route('/api/admin/detections/<int:detection_id>', methods=['DELETE'])
@require_auth(admin_only=True)
def delete_detection(detection_id):
    deleted = Detection.delete_detection(detection_id)
    if not deleted:
        return jsonify({'success': False, 'message': 'Detection record not found.'}), 404

    return jsonify({
        'success': True,
        'message': 'Detection record deleted successfully.'
    }), 200
