from models.mymodelview import MyModelView
from flask_login import current_user
from flask import redirect, url_for, request

class MyAdminProjectView(MyModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.login', next=request.url))