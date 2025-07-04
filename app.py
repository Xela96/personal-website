from flask import Flask, json, render_template, flash, redirect, url_for, request, jsonify
from flask_mail import Mail, Message
from ContactForm import ContactForm
import csv, os
from dotenv import load_dotenv

#load_dotenv("..\.env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv("SENDER_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'jbloggo96@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

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

def load_projects():
    path = os.path.join(os.path.dirname(__file__), 'projects.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)

@app.route('/projects')
def projects():
    projects_data = load_projects() 

    text = request.args.get('searchText', '')
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" and text:
        filtered = [
            project for project in projects_data if text.lower() in project['title'].lower()
        ]
        cards_html = ''.join(
            render_template('_project_card.html', project=project)
            for project in filtered
        )
        return jsonify({"results": [cards_html]})

    return render_template('projects.html', projects=projects_data)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))