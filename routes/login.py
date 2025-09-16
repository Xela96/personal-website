from urllib.parse import urlparse, urljoin
from flask import render_template, flash, redirect, url_for, request, Blueprint
from LoginForm import LoginForm
from flask_login import login_user
from models.user import User
from extensions import csrf, login_manager

login_bp = Blueprint("login", __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ('http', 'https') and
        ref_url.netloc == test_url.netloc
    )

@login_manager.user_loader
def load_user(user_id):
    print(f"[DEBUG] user_loader called with: {user_id}")
    return User.get(user_id)

@csrf.exempt
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.validate(loginForm.loginEmail.data, loginForm.password.data)
        if user:
            login_user(user)
            flash('Login successful', 'success')
            next = request.args.get('next')
            if next and is_safe_url(next):
                return redirect(next)
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template("login.html", form=loginForm)

