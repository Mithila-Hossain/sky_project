# Sky Project

A Django web application for our coursework.  
This project contains multiple apps:

- messaging
- organisation
- reports
- schedule
- skyapp
- teams
- visualisation
  
Repository link: https://github.com/Mithila-Hossain/sky_project.git
This repository contains the full Django project setup, including all apps, settings, and configuration.


## How to run the project

1. Create a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Apply migrations:
   python manage.py migrate

4. Start the server:
   python manage.py runserver

## Notes
- Only work on your own assigned feature so we don’t overwrite each other’s code on the main branch.
- Do not push `venv/` or `db.sqlite3` — they are already ignored.
- Always run `git pull` before pushing your changes.
- After pulling, push your updates using `git push`.


