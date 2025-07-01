class Project:
    def __init__(self, title, description, technologies):
        self.title = title
        self.description = description
        self.technologies = technologies

    def get_project_info(self):
        return {
            "title": self.title,
            "description": self.description,
            "technologies": self.technologies
        }