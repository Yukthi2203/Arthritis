from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db import supabase
from datetime import date, datetime

patient_bp = Blueprint('patient', __name__)

@patient_bp.context_processor
def inject_now():
    return {'now_hour': datetime.now().hour}

# ── Helpers ──────────────────────────────────────────────────────
def db_fetch(table, user_id, order_col='id', limit=None):
    try:
        q = supabase.table(table).select('*').eq('user_id', user_id).order(order_col, desc=True)
        if limit: q = q.limit(limit)
        return q.execute().data or []
    except Exception as e:
        print(f"DB fetch error [{table}]: {e}")
        return []

def db_insert(table, data):
    try:
        supabase.table(table).insert(data).execute()
        return True
    except Exception as e:
        print(f"DB insert error [{table}]: {e}")
        return False

def safe_float(val):
    try: return float(val) if val else None
    except: return None

def get_patient_context(uid):
    """Fetch arthritis type and latest pain score for a user"""
    try:
        profile_res = supabase.table('health_profile').select('arthritis_type').eq('user_id', uid).execute()
        arthritis_type = profile_res.data[0]['arthritis_type'] if profile_res.data else None
    except:
        arthritis_type = None

    # If no profile, check latest ML prediction
    if not arthritis_type:
        try:
            pred_res = supabase.table('ml_predictions').select('predicted_class').eq('user_id', uid).order('prediction_date', desc=True).limit(1).execute()
            arthritis_type = pred_res.data[0]['predicted_class'] if pred_res.data else 'Osteoarthritis (OA)'
        except:
            arthritis_type = 'Osteoarthritis (OA)'

    # Latest pain score
    try:
        pain_res = supabase.table('pain_logs').select('pain_score,swelling,fatigue_level,stiffness_duration_mins').eq('user_id', uid).order('log_date', desc=True).limit(1).execute()
        pain_data = pain_res.data[0] if pain_res.data else {}
        pain_score = pain_data.get('pain_score', 3)
    except:
        pain_score = 3
        pain_data  = {}

    return arthritis_type, pain_score, pain_data

# ── Dashboard ────────────────────────────────────────────────────
@patient_bp.route('/dashboard')
@login_required
def dashboard():
    uid   = str(current_user.id)
    today = str(date.today())
    pain     = db_fetch('pain_logs',       uid, 'log_date',        limit=7)
    hr       = db_fetch('heart_rate_logs', uid, 'log_date',        limit=7)
    all_diet = db_fetch('diet_plans',      uid, 'plan_date',       limit=30)
    all_ex   = db_fetch('exercise_plans',  uid, 'plan_date',       limit=30)
    pred     = db_fetch('ml_predictions',  uid, 'prediction_date', limit=1)
    try:
        pr = supabase.table('health_profile').select('*').eq('user_id', uid).execute()
        profile = pr.data[0] if pr.data else None
    except:
        profile = None
    return render_template('patient_dashboard.html',
        pain_logs      = pain,
        hr_logs        = hr,
        diet_today     = [d for d in all_diet if d.get('plan_date') == today],
        exercise_today = [e for e in all_ex   if e.get('plan_date') == today],
        profile        = profile,
        latest_pred    = pred[0] if pred else None
    )

# ── Pain Tracker ─────────────────────────────────────────────────
@patient_bp.route('/pain', methods=['GET', 'POST'])
@login_required
def pain_tracker():
    uid = str(current_user.id)
    if request.method == 'POST':
        ok = db_insert('pain_logs', {
            'user_id':               uid,
            'log_date':              str(date.today()),
            'pain_score':            int(request.form.get('pain_score', 0)),
            'joint_affected':        request.form.get('joint_affected', 'General'),
            'stiffness_duration_mins': int(request.form.get('stiffness_mins') or 0),
            'swelling':              request.form.get('swelling') == 'on',
            'fatigue_level':         int(request.form.get('fatigue_level') or 0),
            'notes':                 request.form.get('notes', '')
        })
        flash('Pain log saved!' if ok else 'Error saving. Try again.', 'success' if ok else 'error')
        return redirect(url_for('patient.pain_tracker'))
    logs = db_fetch('pain_logs', uid, 'log_date', limit=30)
    return render_template('pain_tracker.html', logs=logs)

# ── Heart Rate ───────────────────────────────────────────────────
@patient_bp.route('/heartrate', methods=['GET', 'POST'])
@login_required
def heart_rate():
    uid = str(current_user.id)
    if request.method == 'POST':
        bpm = request.form.get('bpm')
        if not bpm:
            flash('Please enter BPM.', 'error')
            return redirect(url_for('patient.heart_rate'))
        ok = db_insert('heart_rate_logs', {
            'user_id':          uid,
            'log_date':         str(date.today()),
            'log_time':         request.form.get('log_time') or None,
            'bpm':              int(bpm),
            'measurement_type': request.form.get('measurement_type', 'manual')
        })
        flash('Heart rate logged!' if ok else 'Error saving. Try again.', 'success' if ok else 'error')
        return redirect(url_for('patient.heart_rate'))
    logs = db_fetch('heart_rate_logs', uid, 'log_date', limit=30)
    return render_template('heart_rate.html', logs=logs)

# ── Diet Plan ─────────────────────────────────────────────────────
@patient_bp.route('/diet', methods=['GET', 'POST'])
@login_required
def diet_plan():
    uid = str(current_user.id)

    if request.method == 'POST':
        food_item = request.form.get('food_item', '').strip()
        if not food_item:
            flash('Please enter a food item.', 'error')
            return redirect(url_for('patient.diet_plan'))
        ok = db_insert('diet_plans', {
            'user_id':           uid,
            'plan_date':         str(date.today()),
            'meal_type':         request.form.get('meal_type', 'Breakfast'),
            'food_item':         food_item,
            'quantity_grams':    safe_float(request.form.get('quantity_grams')),
            'calories':          safe_float(request.form.get('calories')),
            'anti_inflammatory': request.form.get('anti_inflammatory') == 'on'
        })
        flash('Meal logged!' if ok else 'Error saving meal. Try again.', 'success' if ok else 'error')
        return redirect(url_for('patient.diet_plan'))

    # Get personalised recommendations
    arthritis_type, pain_score, pain_data = get_patient_context(uid)

    # Build symptom flags for explanations
    symptoms = []
    if pain_data.get('swelling'):                          symptoms.append('swelling')
    if (pain_data.get('stiffness_duration_mins') or 0) > 30: symptoms.append('morning_stiffness')
    if (pain_data.get('fatigue_level') or 0) >= 5:        symptoms.append('fatigue')

    # Check blood report markers
    try:
        blood = supabase.table('blood_reports').select('crp,esr,rf_factor,uric_acid').eq('user_id', uid).order('report_date', desc=True).limit(1).execute()
        if blood.data:
            b = blood.data[0]
            if b.get('crp')       and float(b['crp'])       > 10:  symptoms.append('crp')
            if b.get('esr')       and float(b['esr'])       > 20:  symptoms.append('esr')
            if b.get('rf_factor') and float(b['rf_factor']) > 14:  symptoms.append('rf_factor')
            if b.get('uric_acid') and float(b['uric_acid']) > 7.0: symptoms.append('uric_acid')
    except:
        pass

    from ml.recommendations import get_recommendations
    recs = get_recommendations(arthritis_type, pain_score, symptoms)

    today     = str(date.today())
    all_meals = db_fetch('diet_plans', uid, 'plan_date', limit=50)
    today_meals = [m for m in all_meals if m.get('plan_date') == today]

    return render_template('diet_plan.html',
        meals          = today_meals,
        arthritis_type = arthritis_type,
        pain_score     = pain_score,
        recs           = recs
    )

# ── Exercise Plan ─────────────────────────────────────────────────
@patient_bp.route('/exercise', methods=['GET', 'POST'])
@login_required
def exercise_plan():
    uid = str(current_user.id)

    if request.method == 'POST':
        exercise_name = request.form.get('exercise_name', '').strip()
        if not exercise_name:
            flash('Please enter an exercise name.', 'error')
            return redirect(url_for('patient.exercise_plan'))
        ok = db_insert('exercise_plans', {
            'user_id':       uid,
            'plan_date':     str(date.today()),
            'exercise_name': exercise_name,
            'exercise_type': request.form.get('exercise_type', 'walk'),
            'duration_mins': int(request.form.get('duration_mins') or 0) or None,
            'steps_count':   int(request.form.get('steps_count') or 0) or None,
            'intensity':     request.form.get('intensity', 'low'),
            'pain_before':   int(request.form.get('pain_before') or 0),
            'completed':     request.form.get('completed') == 'on'
        })
        flash('Exercise logged!' if ok else 'Error saving. Try again.', 'success' if ok else 'error')
        return redirect(url_for('patient.exercise_plan'))

    arthritis_type, pain_score, pain_data = get_patient_context(uid)

    from ml.recommendations import get_recommendations, get_pain_level
    recs = get_recommendations(arthritis_type, pain_score)
    pain_level = get_pain_level(pain_score)

    today    = str(date.today())
    all_ex   = db_fetch('exercise_plans', uid, 'plan_date', limit=50)
    today_ex = [e for e in all_ex if e.get('plan_date') == today]

    return render_template('exercise_plan.html',
        exercises      = today_ex,
        arthritis_type = arthritis_type,
        pain_score     = pain_score,
        pain_level     = pain_level,
        recs           = recs
    )

# ── Upload ────────────────────────────────────────────────────────
@patient_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_report():
    uid = str(current_user.id)
    if request.method == 'POST':
        file        = request.files.get('report_file')
        report_type = request.form.get('report_type', 'blood')
        report_date = request.form.get('report_date') or str(date.today())
        if not file or file.filename == '':
            flash('Please select a file.', 'error')
            return redirect(url_for('patient.upload_report'))
        try:
            filename = f"{uid}_{report_date}_{file.filename}".replace(' ', '_')
            bucket   = 'blood-reports' if report_type == 'blood' else 'xrays'
            supabase.storage.from_(bucket).upload(
                path=filename, file=file.read(),
                file_options={'content-type': file.content_type or 'application/octet-stream'}
            )
            file_path = f"{bucket}/{filename}"
            if report_type == 'xray':
                db_insert('xray_uploads', {'user_id': uid, 'upload_date': report_date,
                    'body_part': request.form.get('body_part', 'Unknown'),
                    'file_path': file_path, 'file_type': 'xray'})
            else:
                db_insert('blood_reports', {'user_id': uid, 'report_date': report_date,
                    'rbc': safe_float(request.form.get('rbc')),
                    'wbc': safe_float(request.form.get('wbc')),
                    'hemoglobin': safe_float(request.form.get('hemoglobin')),
                    'esr': safe_float(request.form.get('esr')),
                    'crp': safe_float(request.form.get('crp')),
                    'uric_acid': safe_float(request.form.get('uric_acid')),
                    'rf_factor': safe_float(request.form.get('rf_factor')),
                    'file_path': file_path, 'file_type': file.content_type})
            flash('Report uploaded!', 'success')
        except Exception as e:
            flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('patient.upload_report'))

    reports = db_fetch('blood_reports', uid, 'report_date', limit=20)
    xrays   = db_fetch('xray_uploads',  uid, 'upload_date', limit=20)
    return render_template('upload_report.html', reports=reports, xrays=xrays)

# ── Monitoring ────────────────────────────────────────────────────
@patient_bp.route('/monitoring')
@login_required
def monitoring():
    uid = str(current_user.id)
    return render_template('monitoring.html',
        pain_logs   = db_fetch('pain_logs',       uid, 'log_date',        limit=30),
        hr_logs     = db_fetch('heart_rate_logs',  uid, 'log_date',        limit=30),
        diet_logs   = db_fetch('diet_plans',       uid, 'plan_date',       limit=30),
        ex_logs     = db_fetch('exercise_plans',   uid, 'plan_date',       limit=30),
        predictions = db_fetch('ml_predictions',   uid, 'prediction_date', limit=5)
    )
