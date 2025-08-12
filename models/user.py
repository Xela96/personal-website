from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

class User(UserMixin):
    users = {
        "admin@example.com": {"password": "password123"}
    }

    def __init__(self, id):
        self.id = id

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