# routes/auth.py — Login, Register, Logout

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from db import supabase
from models.user import User

auth_bp = Blueprint('auth', __name__)

# ── Import bcrypt from app (avoids double-init) ──────────────────
def get_bcrypt():
    from app import bcrypt
    return bcrypt

# ── Landing Page ─────────────────────────────────────────────────
@auth_bp.route('/')
def landing():
    return render_template('landing.html')

# ── Register ─────────────────────────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email     = request.form.get('email', '').strip().lower()
        password  = request.form.get('password', '')
        role      = request.form.get('role', 'patient')
        age       = request.form.get('age') or None
        gender    = request.form.get('gender') or None

        # Check duplicate email
        existing = supabase.table('users').select('id').eq('email', email).execute()
        if existing.data:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('auth.register'))

        hashed_pw = get_bcrypt().generate_password_hash(password).decode('utf-8')

        supabase.table('users').insert({
            'full_name':     full_name,
            'email':         email,
            'password_hash': hashed_pw,
            'role':          role,
            'age':           age,
            'gender':        gender
        }).execute()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# ── Login ─────────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        response = supabase.table('users').select('*').eq('email', email).execute()

        if not response.data:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth.login'))

        user_data = response.data[0]

        if get_bcrypt().check_password_hash(user_data['password_hash'], password):
            user = User(user_data)
            login_user(user)
            # Redirect based on role
            if user.is_doctor():
                return redirect(url_for('doctor.dashboard'))
            return redirect(url_for('patient.dashboard'))

        flash('Invalid email or password.', 'error')

    return render_template('login.html')

# ── Logout ───────────────────────────────────────────────────────
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.landing'))
