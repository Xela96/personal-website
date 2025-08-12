from flask import Blueprint, render_template
from models.project import Project

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/projects")
def projects():
    projects_list = Project.query.filter_by(is_published=True).order_by(Project.date_created.desc()).all()
    return render_template('projects.html', projects=projects_list)