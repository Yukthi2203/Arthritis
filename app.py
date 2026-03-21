# # app.py — ArthriCare Main Application Entry Point

# from flask import Flask
# from flask_login import LoginManager
# from db import supabase
# from routes.auth import auth_bp
# from routes.patient import patient_bp
# from routes.doctor import doctor_bp
# from routes.ml_routes import ml_bp
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY", "arthricare-secret-key-change-in-production")

# # ── Register Blueprints ──────────────────────────────────────────
# app.register_blueprint(auth_bp)          # /login  /register  /logout
# app.register_blueprint(patient_bp)       # /dashboard  /pain  /diet  /exercise  /upload  /heartrate
# app.register_blueprint(doctor_bp)        # /doctor/dashboard  /doctor/patients
# app.register_blueprint(ml_bp)            # /predict  /results

# # ── Flask-Login Setup ────────────────────────────────────────────
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# from models.user import User

# @login_manager.user_loader
# def load_user(user_id):
#     response = supabase.table('users').select('*').eq('id', user_id).execute()
#     if response.data:
#         return User(response.data[0])
#     return None

# if __name__ == '__main__':
#     app.run(debug=True)

# app.py — ArthriCare Main Application Entry Point

import os
from dotenv import load_dotenv
load_dotenv()  # ← must be FIRST before anything else reads env vars

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# ── App Init ─────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "arthricare-secret-key-change-in-production")

# ── Extensions ───────────────────────────────────────────────────
bcrypt = Bcrypt(app)   # initialise bcrypt on the app instance

# ── Supabase ─────────────────────────────────────────────────────
from db import supabase

# ── Blueprints ───────────────────────────────────────────────────
from routes.auth     import auth_bp
from routes.patient  import patient_bp
from routes.doctor   import doctor_bp
from routes.ml_routes import ml_bp

app.register_blueprint(auth_bp)      # /  /login  /register  /logout
app.register_blueprint(patient_bp)   # /dashboard  /pain  /heartrate  /diet  /exercise  /upload  /monitoring
app.register_blueprint(doctor_bp)    # /doctor/dashboard  /doctor/patient/<id>
app.register_blueprint(ml_bp)        # /predict  /predict/api

# ── Flask-Login ──────────────────────────────────────────────────
from models.user import User

login_manager = LoginManager()
login_manager.login_view   = 'auth.login'     # redirect here if not logged in
login_manager.login_message = 'Please log in to access ArthriCare.'
login_manager.login_message_category = 'error'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Reload user from DB on every request using their UUID."""
    try:
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if response.data:
            return User(response.data[0])
    except Exception:
        pass
    return None

# ── Run ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
