from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    loginEmail = EmailField('', validators=[DataRequired(), Email(), Length(min=3, max=60)], render_kw={"placeholder": "Your Email"})
    password = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')