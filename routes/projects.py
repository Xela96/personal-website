from flask import Blueprint, render_template, request,jsonify
from models.project import Project

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/projects")
def projects():
    projects_list = Project.query.filter_by(is_published=True).order_by(Project.date_created.desc()).all()

    text = request.args.get('searchText', '')
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" and text:
        filtered = [
            project for project in projects_list if text.lower() in project.title.lower()
        ]
        cards_html = ''.join(
            render_template('_project_card.html', project=project)
            for project in filtered
        )
        return jsonify({"results": [cards_html]})
    
    return render_template('projects.html', projects=projects_list)