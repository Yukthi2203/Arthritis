# ml/hybrid_model.py — Hybrid SVM + Random Forest Arthritis Classifier
# Matches exactly the pipeline diagram provided

import numpy as np
import pickle
import os
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# ── Class Labels ─────────────────────────────────────────────────
ARTHRITIS_CLASSES = [
    'Osteoarthritis (OA)',
    'Rheumatoid Arthritis (RA)',
    'Gout',
    'Psoriatic Arthritis',
    'Ankylosing Spondylitis',
    'Juvenile Idiopathic Arthritis',
    'No Arthritis Detected'
]

RISK_THRESHOLDS = {
    'high':     0.75,
    'moderate': 0.50,
    'low':      0.0
}

MODEL_PATH  = os.path.join(os.path.dirname(__file__), 'saved_models', 'hybrid_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'saved_models', 'scaler.pkl')

# ── Build Hybrid Model ───────────────────────────────────────────
def build_hybrid_model():
    """
    Creates a Voting Classifier combining:
      - SVM  (Support Vector Machine)
      - Random Forest
    Both soft-vote for final prediction (as per pipeline diagram)
    """
    svm_model = SVC(
        kernel='rbf',
        probability=True,   # needed for soft voting
        C=10,
        gamma='scale',
        random_state=42
    )

    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )

    hybrid = VotingClassifier(
        estimators=[
            ('svm', svm_model),
            ('random_forest', rf_model)
        ],
        voting='soft',      # averages predicted probabilities
        weights=[1, 1]      # equal weight to both models
    )

    return hybrid

# ── Train Model ──────────────────────────────────────────────────
def train_model(X_train, y_train):
    """
    Train the hybrid model and save it.
    Features (in order):
      pain_score, stiffness_mins, swelling, fatigue,
      age, crp, esr, uric_acid, rf_factor
    """
    os.makedirs(os.path.join(os.path.dirname(__file__), 'saved_models'), exist_ok=True)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    model = build_hybrid_model()
    model.fit(X_scaled, y_train)

    with open(MODEL_PATH, 'wb')  as f: pickle.dump(model, f)
    with open(SCALER_PATH, 'wb') as f: pickle.dump(scaler, f)

    print("Model trained and saved.")
    return model, scaler

# ── Load Saved Model ─────────────────────────────────────────────
def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, 'rb')  as f: model  = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f: scaler = pickle.load(f)
        return model, scaler
    return None, None

# ── Predict ──────────────────────────────────────────────────────
def predict_arthritis(features: list) -> dict:
    """
    Takes a list of 9 feature values and returns prediction.
    Features: [pain_score, stiffness_mins, swelling, fatigue,
               age, crp, esr, uric_acid, rf_factor]
    """
    model, scaler = load_model()

    if model is None:
        # Fallback: rule-based prediction if model not trained yet
        return _rule_based_fallback(features)

    X = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)

    pred_idx    = model.predict(X_scaled)[0]
    proba       = model.predict_proba(X_scaled)[0]
    confidence  = float(np.max(proba))
    pred_class  = ARTHRITIS_CLASSES[pred_idx]
    risk_level  = _get_risk_level(confidence)

    return {
        'predicted_class': pred_class,
        'confidence':      round(confidence * 100, 2),
        'risk_level':      risk_level,
        'all_proba':       {cls: round(float(p)*100, 2) for cls, p in zip(ARTHRITIS_CLASSES, proba)},
        'model_used':      'Hybrid SVM + Random Forest',
        'gradcam_path':    None
    }

# ── Evaluate Model ───────────────────────────────────────────────
def evaluate_model(X_test, y_test):
    model, scaler = load_model()
    if model is None:
        return {}

    X_scaled = scaler.transform(X_test)
    y_pred   = model.predict(X_scaled)

    return {
        'accuracy':  round(accuracy_score(y_test, y_pred), 4),
        'f1_score':  round(f1_score(y_test, y_pred, average='weighted'), 4),
        'precision': round(precision_score(y_test, y_pred, average='weighted'), 4),
        'recall':    round(recall_score(y_test, y_pred, average='weighted'), 4)
    }

# ── Helpers ──────────────────────────────────────────────────────
def _get_risk_level(confidence):
    if confidence >= RISK_THRESHOLDS['high']:     return 'high'
    if confidence >= RISK_THRESHOLDS['moderate']: return 'moderate'
    return 'low'

def _rule_based_fallback(features):
    """Simple rule engine when ML model isn't trained yet"""
    pain, stiffness, swelling, fatigue, age, crp, esr, uric_acid, rf_factor = features

    if uric_acid > 7.0:
        pred = 'Gout'
    elif rf_factor > 20 or (crp > 10 and stiffness > 60):
        pred = 'Rheumatoid Arthritis (RA)'
    elif age > 50 and pain > 5:
        pred = 'Osteoarthritis (OA)'
    else:
        pred = 'No Arthritis Detected'

    return {
        'predicted_class': pred,
        'confidence':      65.0,
        'risk_level':      'moderate',
        'all_proba':       {},
        'model_used':      'Rule-Based Fallback',
        'gradcam_path':    None
    }
