from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
from wtforms import Form, FileField, StringField
from wtforms.validators import DataRequired

class DownloadFileForm(Form):
    filename = StringField('Filename', validators=[DataRequired()])
    data = FileField('File')

class MyAdminDownloadFileView(ModelView):
    form = DownloadFileForm
    form_columns = ('filename', 'data')
    column_list = ('filename', 'uploaded_at')

    def on_model_change(self, form, model, is_created):
        file_data = form.data.data
        if file_data:
            model.data = file_data.read()
        elif not is_created:
            pass
        return super().on_model_change(form, model, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "is_admin", False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.login', next=request.url))