# routes/doctor.py — Doctor / Researcher Dashboard

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from db import supabase
from functools import wraps

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

def doctor_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_doctor():
            return render_template('landing.html'), 403
        return f(*args, **kwargs)
    return decorated

@doctor_bp.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    patients     = supabase.table('users').select('*').eq('role', 'patient').execute()
    recent_preds = supabase.table('ml_predictions').select('*').order('prediction_date', desc=True).limit(20).execute()
    total_pain   = supabase.table('pain_logs').select('user_id, pain_score').execute()
    return render_template('doctor_dashboard.html',
        patients     = patients.data,
        predictions  = recent_preds.data,
        pain_summary = total_pain.data
    )

@doctor_bp.route('/patient/<int:patient_id>')
@login_required
@doctor_required
def view_patient(patient_id):
    user    = supabase.table('users').select('*').eq('id', patient_id).execute()
    profile = supabase.table('health_profile').select('*').eq('user_id', patient_id).execute()
    pain    = supabase.table('pain_logs').select('*').eq('user_id', patient_id).order('log_date', desc=True).limit(30).execute()
    blood   = supabase.table('blood_reports').select('*').eq('user_id', patient_id).order('report_date', desc=True).execute()
    preds   = supabase.table('ml_predictions').select('*').eq('user_id', patient_id).order('prediction_date', desc=True).execute()
    hr      = supabase.table('heart_rate_logs').select('*').eq('user_id', patient_id).order('log_date', desc=True).limit(30).execute()

    return render_template('doctor_patient_view.html',
        patient  = user.data[0] if user.data else None,
        profile  = profile.data[0] if profile.data else None,
        pain     = pain.data,
        blood    = blood.data,
        preds    = preds.data,
        hr       = hr.data
    )
