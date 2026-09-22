# [VET-FEATURE] new file — vet blueprint
from flask import Blueprint, g, jsonify, request

from app.models.detection import Detection
from app.models.vet_review import VetReview
from app.utils.auth import require_auth

vet_bp = Blueprint('vet', __name__)


def _vet_only():
    """Return True if the current user is a vet or admin."""
    return g.current_user['role'] in ('vet', 'admin')


@vet_bp.route('/api/vet/summary', methods=['GET'])
@require_auth()
def vet_summary():
    if not _vet_only():
        return jsonify({'success': False, 'message': 'Vet access required.'}), 403

    summary = VetReview.get_vet_summary(g.current_user['id'])
    return jsonify({'success': True, 'summary': summary}), 200


@vet_bp.route('/api/vet/queue', methods=['GET'])
@require_auth()
def vet_queue():
    """All detections with their latest review for the current vet."""
    if not _vet_only():
        return jsonify({'success': False, 'message': 'Vet access required.'}), 403

    detections = Detection.get_all_detections()

    # Build a lookup of detection_id → latest review for this vet
    vet_reviews = VetReview.get_all_reviews(vet_id=g.current_user['id'])
    review_map = {}
    for r in vet_reviews:
        did = r['detection_id']
        if did not in review_map:
            review_map[did] = r

    result = []
    for d in detections:
        item = {
            **d,
            'detected_at': str(d['detected_at']),
            'image_url': f"/uploads/{d['image_name']}" if d['image_name'] else '',
            'latest_review': None
        }
        if d['id'] in review_map:
            rev = review_map[d['id']]
            item['latest_review'] = {
                **rev,
                'reviewed_at': str(rev['reviewed_at'])
            }
        result.append(item)

    return jsonify({'success': True, 'detections': result, 'total': len(result)}), 200


@vet_bp.route('/api/vet/reviews', methods=['POST'])
@require_auth()
def create_or_update_review():
    if not _vet_only():
        return jsonify({'success': False, 'message': 'Vet access required.'}), 403

    data = request.get_json() or {}

    detection_id = data.get('detection_id')
    if not detection_id:
        return jsonify({'success': False, 'message': 'detection_id is required.'}), 400

    status = (data.get('status') or 'pending').strip().lower()
    if status not in VetReview.REVIEW_STATUSES:
        return jsonify({
            'success': False,
            'message': f"Status must be one of: {', '.join(sorted(VetReview.REVIEW_STATUSES))}."
        }), 400

    risk_level = (data.get('risk_level') or 'medium').strip().lower()
    if risk_level not in VetReview.RISK_LEVELS:
        return jsonify({
            'success': False,
            'message': f"Risk level must be one of: {', '.join(sorted(VetReview.RISK_LEVELS))}."
        }), 400

    review_id = VetReview.upsert_review(
        detection_id=detection_id,
        vet_id=g.current_user['id'],
        status=status,
        risk_level=risk_level,
        diagnosis_notes=data.get('diagnosis_notes') or '',
        recommended_action=data.get('recommended_action') or '',
        needs_lab_test=bool(data.get('needs_lab_test', False)),
        needs_farm_visit=bool(data.get('needs_farm_visit', False)),
        needs_medication_change=bool(data.get('needs_medication_change', False))
    )

    if not review_id:
        return jsonify({'success': False, 'message': 'Failed to save review.'}), 500

    return jsonify({'success': True, 'message': 'Review saved.', 'review_id': review_id}), 200


@vet_bp.route('/api/vet/reviews', methods=['GET'])
@require_auth()
def list_vet_reviews():
    if not _vet_only():
        return jsonify({'success': False, 'message': 'Vet access required.'}), 403

    status_filter = request.args.get('status', '').strip().lower() or None
    reviews = VetReview.get_all_reviews(vet_id=g.current_user['id'], status=status_filter)

    return jsonify({
        'success': True,
        'reviews': [{
            **r,
            'reviewed_at': str(r['reviewed_at'])
        } for r in reviews],
        'total': len(reviews)
    }), 200
