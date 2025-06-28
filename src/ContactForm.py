from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=40)], render_kw={"placeholder": "Your Name"})
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(min=3, max=60)], render_kw={"placeholder": "Your Email"})
    company = TextAreaField('Company', render_kw={"placeholder": "Your Company (Optional)"})
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=20, max=500)], render_kw={"placeholder": "Your Message"})
    submit = SubmitField('Send Message')