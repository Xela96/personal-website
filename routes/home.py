from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from models.homepagecontent import HomepageContent
from ContactForm import ContactForm
from flask_mail import Message
import os
from extensions import mail

homepage_bp = Blueprint("home", __name__, template_folder='templates')

@homepage_bp.route("/", methods=['GET', 'POST'])
def home():
    try:
        about = HomepageContent.query.filter_by(section_name="about_me").first()
        experience = HomepageContent.query.filter_by(section_name="experience").first()
    except Exception as e:
        print("Database query error:", e)
        return "DB error", 500

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
        return redirect(url_for('home.home'))

    return render_template('index.html', form=form, about=about, experience=experience)