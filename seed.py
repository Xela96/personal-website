import os
from app import create_app, db
from app import Project, HomepageContent
from models.downloadfile import DownloadFile

app = create_app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CV_FILE_PATH = os.path.join(BASE_DIR, 'static', 'files', 'CV_AlexDoherty.pdf')

with app.app_context():
    db.create_all()

    new_project = Project(
        title="Playwright tests",
        description="An automated test framework built with Playwright to test a Flask web application. Tests created for form validation, email delivery, file download, dynamic search and filtering and more.",
        technologies=["Typescript", "Playwright", "Github CI", "Google Cloud Console"],
        github_url="https://github.com/Xela96/playwright-tests",
        is_published=True
    )
    db.session.add(new_project)
    db.session.commit()
    print("Project added!")

    new_project = Project(
        title="Personal Portfolio Website",
        description="A website to showcase my projects and skills.",
        technologies=["Python", "Flask", "HTML", "CSS"],
        github_url="https://github.com/Xela96/playwright-tests",
        is_published=True
    )
    db.session.add(new_project)
    db.session.commit()
    print("Project added!")

    new_project = Project(
        title="Simulation Engine Test Framework",
        description="An automated test framework for automated UI, API and result testing of an energy performance simulation engine.",
        technologies=["CSharp", "SpecFlow", "WinAppDriver", "Azure Pipeline"],
        is_published=True
    )
    db.session.add(new_project)
    db.session.commit()
    print("Project added!")

    new_project = Project(
        title="Automated Fluid Tester",
        description="Test library development for automated testing of fluidics medical device. Created test methods to test subsystem requirements of R&D product for design verification. CSharp and Python development for interaction with R&D product, Python script for UI automation and CSharp development for a human-machine interface.",
        technologies=["Python", "Squish for Python", "CSharp"],
        is_published=True
    )
    db.session.add(new_project)
    db.session.commit()
    print("Project added!")

    homepage_data = [
        {
            "section_name": "about_me",
            "text_content": "Welcome to my personal website! Feel free to mess around with any of the features and let me know if you find any issues through the contact me form. I am a Software Engineer with 4+ years of experience developing automation manufacturing applications and automated test frameworks using <strong>C# .NET</strong> and <strong>Python</strong>. Passionate about test automation, solving real-life problems and making a difference to the world in my career. Currently focused on test automation and quality assurance. Industry experience in testing includes medical devices, performance and simulation system software and retail. "
        },
        {
            "section_name": "experience",
            "text_content": "Throughout my career, I have worked on numerous projects that have honed my skills in software development and test automation. I have used Squish for Python for UI test automation of QT built applications and WindowsApplicationDriver for Selenium-like UI test automation of Windows applications. Working in the medical devices industry on devices such as pacemakers, defibrillators and dialysis machines has brought me a strict level of quality to my testing, knowing the importance of a product being released as intended. "
        }
    ]

    for content in homepage_data:
        if not HomepageContent.query.filter_by(section_name=content["section_name"]).first():
            db.session.add(HomepageContent(**content))
    db.session.commit()
    print("Homepage content seeded!")

    from models.downloadfile import DownloadFile

    if os.path.exists(CV_FILE_PATH):
        with open(CV_FILE_PATH, 'rb') as f:
            file_bytes = f.read()

        if not DownloadFile.query.filter_by(filename="CV_AlexDoherty.pdf").first():
            cv_file = DownloadFile(filename="CV_AlexDoherty.pdf", data=file_bytes)
            db.session.add(cv_file)
            db.session.commit()
            print("CV file added!")
    else:
        print(f"CV file not found at {CV_FILE_PATH}")
