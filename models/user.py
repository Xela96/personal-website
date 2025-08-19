from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from extensions import db

class User(UserMixin):
    # id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    # password = db.Column(db.String(128), nullable=False)
    # is_admin = db.Column(db.Boolean, default=False)
    users = {
        "admin@example.com": {"password": "password123", "is_admin": True}
    }

    def __init__(self, email):
        self.id = email
        self.email = email
        self.password = self.users[email]["password"]
        self._is_admin = self.users[email]["is_admin"]

    @property
    def is_admin(self):
        return self._is_admin

    @classmethod
    def get(cls, id):
        if id in cls.users:
            return cls(id)
        return None

    @classmethod
    def validate(cls, email, password):
        user = cls.users.get(email)
        if user and user["password"] == password:
            return cls(email)
        return None