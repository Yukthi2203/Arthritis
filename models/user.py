# models/user.py — Flask-Login User Model

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, data):
        self.id = str(data['id'])
        self.full_name = data['full_name']
        self.email = data['email']
        self.role = data.get('role', 'patient')   # 'patient' or 'doctor'

    def is_doctor(self):
        return self.role == 'doctor'
