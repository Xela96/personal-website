from flask import Flask
import os
import os.path as op
from flask_admin import Admin 
from extensions import db, mail, login_manager, csrf
from models.homepagecontent import HomepageContent
from models.project import Project
from models.downloadfile import DownloadFile
from routes.home import homepage_bp
from routes.login import login_bp
from routes.logout import logout_bp
from routes.projects import projects_bp
from models.admin.myadminhomepageview import MyAdminHomepageView
from models.admin.myadminindexview import MyAdminIndexView
from models.admin.myfileadminview import MyFileAdminView
from models.admin.myadminprojectview import MyAdminProjectView
from dotenv import load_dotenv
load_dotenv()

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"))

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
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    db_user = os.getenv("SUPABASE_USER")
    db_password = os.getenv("SUPABASE_PASSWORD")
    db_host = os.getenv("SUPABASE_HOST")
    db_port = os.getenv("SUPABASE_PORT")
    db_name = os.getenv("SUPABASE_DB")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(homepage_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(projects_bp)

    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    db.init_app(app)

    csrf.init_app(app)

    admin = Admin(app, name='personal-website', index_view=MyAdminIndexView(), template_mode='bootstrap3')
    init_admin(admin, app)

    return app

def init_admin(admin, app):
    path = op.join(op.dirname(__file__), 'static/files')

    admin.add_view(MyFileAdminView(path, '/static/files', name='Static Files'))

    admin.add_view(MyAdminProjectView(Project, db.session))
    admin.add_view(MyAdminHomepageView(HomepageContent, db.session))

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)