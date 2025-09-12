from extensions import db
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from flask import json

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.JSON)
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