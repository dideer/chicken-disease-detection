import os
import uuid

from flask import Blueprint, jsonify, request
import gdown
import numpy as np
from PIL import Image
import tensorflow as tf

from app.models.detection import Detection
from app.models.user import User

predict_bp = Blueprint('predict', __name__)

BASE_DIR      = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH    = os.path.join(BASE_DIR, 'chicken_cnn_final.tflite')
FILTER_PATH   = os.path.join(BASE_DIR, 'filter_cnn.tflite')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'frontend', 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Download Disease CNN ──────────────────────────────────────────────────────
if not os.path.exists(MODEL_PATH):
    print("[INFO] Downloading Disease CNN...")
    try:
        gdown.download(
            id="1RhX6Ea_f0xLkjvqThiE_HqEQAbgXZOLO",
            output=MODEL_PATH, quiet=False)
        print("[INFO] Disease CNN downloaded.")
    except Exception as exc:
        print(f"[WARN] Could not download Disease CNN: {exc}")
else:
    print("[INFO] Disease CNN already exists.")

# ── Download Filter CNN ───────────────────────────────────────────────────────
if not os.path.exists(FILTER_PATH):
    print("[INFO] Downloading Filter CNN...")
    try:
        gdown.download(
            id="1yRseVKg0GsL_xRzfQ8FUetoUccUpni4Q",
            output=FILTER_PATH, quiet=False)
        print("[INFO] Filter CNN downloaded.")
    except Exception as exc:
        print(f"[WARN] Could not download Filter CNN: {exc}")
else:
    print("[INFO] Filter CNN already exists.")

# ── Load Disease CNN (TFLite) ─────────────────────────────────────────────────
interpreter    = None
input_details  = None
output_details = None

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details  = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("[INFO] Disease CNN loaded successfully.")
except Exception as exc:
    interpreter = None
    print(f"[ERROR] Failed to load Disease CNN: {exc}")

# ── Load Filter CNN (TFLite) ──────────────────────────────────────────────────
filter_interpreter    = None
filter_input_details  = None
filter_output_details = None

try:
    filter_interpreter = tf.lite.Interpreter(model_path=FILTER_PATH)
    filter_interpreter.allocate_tensors()
    filter_input_details  = filter_interpreter.get_input_details()
    filter_output_details = filter_interpreter.get_output_details()
    print("[INFO] Filter CNN loaded successfully.")
except Exception as exc:
    filter_interpreter = None
    print(f"[ERROR] Failed to load Filter CNN: {exc}")

# ── Constants ─────────────────────────────────────────────────────────────────
CLASSES = ['crd', 'fowlpox', 'healthy']

ADVICE = {
    'crd': {
        'full_name': 'Chronic Respiratory Disease (CRD)',
        'symptoms': 'Nasal discharge, coughing, swollen face, breathing difficulty',
        'urgency': 'High - Act within 24 hours',
        'treatment': [
            'Isolate infected birds immediately',
            'Administer Tylosin or Oxytetracycline antibiotics',
            'Improve ventilation in the poultry house',
            'Consult a veterinarian for proper dosage',
            'Disinfect the poultry house thoroughly'
        ]
    },
    'fowlpox': {
        'full_name': 'Fowl Pox',
        'symptoms': 'Wart-like lesions on comb, face, and legs',
        'urgency': 'Medium - Act within 48 hours',
        'treatment': [
            'Isolate infected birds from healthy flock',
            'Apply iodine solution to lesions',
            'Vaccinate healthy birds immediately',
            'Provide vitamin A supplements',
            'Keep wounds clean to prevent secondary infections'
        ]
    },
    'healthy': {
        'full_name': 'Healthy Chicken',
        'symptoms': 'No disease symptoms detected',
        'urgency': 'None - Continue routine care',
        'treatment': [
            'Continue regular feeding schedule',
            'Maintain clean water supply',
            'Keep poultry house well ventilated',
            'Monitor flock regularly',
            'Keep vaccination schedule up to date'
        ]
    }
}


def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(img_array, axis=0)


def run_filter_cnn(image_path):
    img_array = preprocess_image(image_path)
    filter_interpreter.set_tensor(
        filter_input_details[0]['index'], img_array)
    filter_interpreter.invoke()
    pred = filter_interpreter.get_tensor(
        filter_output_details[0]['index'])
    return float(pred[0][0])


def run_disease_cnn(image_path):
    img_array = preprocess_image(image_path)
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])[0]


@predict_bp.route('/api/predict', methods=['POST'])
def predict():
    if interpreter is None:
        return jsonify({'success': False,
                        'message': 'Disease CNN not available'}), 500
    if filter_interpreter is None:
        return jsonify({'success': False,
                        'message': 'Filter CNN not available'}), 500
    if 'file' not in request.files:
        return jsonify({'success': False,
                        'message': 'No image uploaded'}), 400

    file     = request.files['file']
    username = request.form.get('username', 'unknown')
    user     = User.find_by_username(username) if username and username != 'unknown' else None

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    try:
        ext         = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        filepath    = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(filepath)

        # Step 1 — Filter CNN
        filter_score = run_filter_cnn(filepath)
        if filter_score > 0.5:
            return jsonify({
                'success': False,
                'message': 'No chicken detected. Please upload a chicken image.'
            }), 400

        # Step 2 — Disease CNN
        predictions     = run_disease_cnn(filepath)
        predicted_index = int(np.argmax(predictions))
        predicted_class = CLASSES[predicted_index]
        confidence      = float(predictions[predicted_index]) * 100
        crd_prob        = float(predictions[0]) * 100
        fowlpox_prob    = float(predictions[1]) * 100
        healthy_prob    = float(predictions[2]) * 100

        Detection.save_detection(
            user_id=user['id'] if user else None,
            username=username,
            image_name=unique_name,
            predicted_class=predicted_class,
            confidence=round(confidence, 2),
            crd_prob=round(crd_prob, 2),
            fowlpox_prob=round(fowlpox_prob, 2),
            healthy_prob=round(healthy_prob, 2),
            chicken_count=1
        )

        return jsonify({
            'success': True,
            'predicted_class': predicted_class,
            'confidence': round(confidence, 2),
            'probabilities': {
                'crd':     round(crd_prob, 2),
                'fowlpox': round(fowlpox_prob, 2),
                'healthy': round(healthy_prob, 2)
            },
            'disease_info': ADVICE[predicted_class],
            'image_name': unique_name
        }), 200

    except Exception as exc:
        return jsonify({'success': False,
                        'message': f'Prediction failed: {exc}'}), 500


@predict_bp.route('/api/history', methods=['GET'])
def history():
    username   = request.args.get('username', None)
    detections = Detection.get_all_detections(username=username)
    return jsonify({
        'success': True,
        'detections': [{
            **item,
            'detected_at': str(item['detected_at'])
        } for item in detections]
    }), 200


@predict_bp.route('/api/statistics', methods=['GET'])
def statistics():
    stats = Detection.get_statistics()
    total = sum(stats.values())
    return jsonify({
        'success': True,
        'statistics': stats,
        'total': total
    }), 200