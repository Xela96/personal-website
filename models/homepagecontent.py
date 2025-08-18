from extensions import db
from datetime import datetime

class HomepageContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.Text, nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, onupdate=datetime.now)