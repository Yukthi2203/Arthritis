# routes/ml_routes.py — ML Prediction Endpoints

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from db import supabase
from datetime import date
import numpy as np

ml_bp = Blueprint('ml', __name__)

@ml_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        input_type = request.form.get('input_type', 'symptoms')

        if input_type == 'symptoms':
            # Build feature vector from symptom form inputs
            features = [
                float(request.form.get('pain_score', 0)),
                float(request.form.get('stiffness_mins', 0)),
                float(request.form.get('swelling', 0)),
                float(request.form.get('fatigue', 0)),
                float(request.form.get('age', 0)),
                float(request.form.get('crp', 0)),
                float(request.form.get('esr', 0)),
                float(request.form.get('uric_acid', 0)),
                float(request.form.get('rf_factor', 0)),
            ]
            from ml.hybrid_model import predict_arthritis
            result = predict_arthritis(features)

        elif input_type == 'xray':
            file = request.files.get('xray_file')
            if file:
                from ml.image_model import predict_from_xray
                result = predict_from_xray(file)
            else:
                result = {'predicted_class': 'Unknown', 'confidence': 0, 'gradcam_path': None}

        # Save prediction to DB
        supabase.table('ml_predictions').insert({
            'user_id':          current_user.id,
            'prediction_date':  str(date.today()),
            'input_type':       input_type,
            'predicted_class':  result['predicted_class'],
            'confidence_score': result['confidence'],
            'risk_level':       result.get('risk_level', 'moderate'),
            'model_used':       result.get('model_used', 'Hybrid SVM+RF'),
            'gradcam_path':     result.get('gradcam_path')
        }).execute()

        return render_template('ml_prediction.html', result=result, submitted=True)

    return render_template('ml_prediction.html', result=None, submitted=False)

@ml_bp.route('/predict/api', methods=['POST'])
@login_required
def predict_api():
    """JSON endpoint for async predictions"""
    data     = request.get_json()
    features = data.get('features', [])
    from ml.hybrid_model import predict_arthritis
    result = predict_arthritis(features)
    return jsonify(result)
