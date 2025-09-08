from app import app, db
from app import Project
from app import HomepageContent

with app.app_context():
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

    # file_path = "static/files/CV_AlexDoherty.pdf"

    # with open(file_path, 'rb') as f:
    #     file_bytes = f.read()

    # new_file = DownloadFile(
    #     filename="CV_AlexDoherty.pdf",
    #     data=file_bytes
    # )

    # db.session.add(new_file)
    # db.session.commit()
    # print("File added!")

    new_text = HomepageContent(
        section_name="about_me",
        text_content="Welcome to my personal website! Feel free to mess around with any of the features and let me know if you find any issues through the contact me form. I am a Software Engineer with 3+ years of experience developing automation manufacturing applications and automated test frameworks using .NET and Python. Passionate about test automation, solving real-life problems and making a difference to the world in my career. Currently focused on full-stack development and test automation. Industry experience includes medical devices as well as performance and simulation system software.",
    )
    db.session.add(new_text)
    db.session.commit()
    print("Content added!")

    new_text = HomepageContent(
        section_name="experience",
        text_content="Throughout my career, I have worked on numerous projects that have honed my skills in software development and test automation. I have used Squish for Python for UI test automation of QT built applications and WindowsApplicationDriver for Selenium-like UI test automation of Windows applications. Working in the medical devices industry on devices such as pacemakers, defibrillators and dialysis machines has brought me a strict level of quality to my testing, knowing the importance of a product being released as intended. ",
    )
    db.session.add(new_text)
    db.session.commit()
    print("Content added!")