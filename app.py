from flask import Flask, json, render_template, flash, redirect, url_for, request, jsonify
from flask_mail import Mail, Message
from ContactForm import ContactForm
from LoginForm import LoginForm
import os
import os.path as op
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from urllib.parse import urlparse, urljoin
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy import LargeBinary
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv("SENDER_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("SENDER_EMAIL")
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)

csrf = CSRFProtect(app)

admin = Admin(app, name='personal-website', template_mode='bootstrap3')

@app.route('/', methods = ['GET', 'POST'])
def home():    
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            subject=form.name.data,
            sender=os.getenv("SENDER_EMAIL"),
            recipients=[os.getenv("RECIPIENT_EMAIL")],
            body=form.message.data + "\n\nFrom: " + form.email.data + "\nName: " + form.name.data,
        )
        try:
            mail.send(msg)
            message = 'Thank you for your message!'
            category = 'success'
        except Exception as e:
            print("Error sending email:", e)
            message = f"Error sending email: {e}"
            category = 'danger'
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({'message': message, 'category': category})
        flash(message, category)
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            print("Form errors:", form.errors)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({'message': 'Form validation failed', 'category': 'danger', 'errors': form.errors})
    return render_template('index.html', form=form)

@app.route('/projects')
def projects():
    projects_list = Project.query.filter_by(is_published=True).order_by(Project.date_created.desc()).all()
    return render_template('projects.html', projects=projects_list)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ('http', 'https') and
        ref_url.netloc == test_url.netloc
    )

@csrf.exempt
@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template("login.html", form=loginForm)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('login'))

# @app.route("/admin")
# @login_required
# def admin():
#     return render_template("admin.html")

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

@login_manager.user_loader
def load_user(user_id):
    print(f"[DEBUG] user_loader called with: {user_id}")
    return User.get(user_id)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(JSON)
    github_url = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)
    last_updated = db.Column(db.DateTime, onupdate=datetime.now)
    is_published = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Project {self.title}>"
    
    def set_technologies(self, tech_list):
        self.technologies = json.dumps(tech_list)

    def get_technologies(self):
        return json.loads(self.technologies or "[]")
    
class DownloadFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    data = db.Column(LargeBinary)
    
path = op.join(op.dirname(__file__), 'static/files')
admin.add_view(FileAdmin(path, '/static/files', name='Static Files'))

admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(DownloadFile, db.session))

