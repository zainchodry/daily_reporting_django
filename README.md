# Daily Reporting System Django

A Django-based daily reporting and task management system with user roles, task assignment, report submission, and notification support.

## Overview

This project is built with Django 5.2 and provides a simple workflow for:

- user registration and authentication
- role-based users: admin, manager, employee
- profile management with photo upload and contact details
- task creation, assignment, status updates, and deletion
- daily report submission, review, approval, and rejection
- notification delivery for task assignments and report status changes

## Features

- Custom email-based user authentication
- User roles and permissions
- Admin/manager dashboard with team metrics
- Employee dashboard with personal task/report summaries
- Task CRUD operations with priority and status tracking
- Daily report submission tied to tasks
- Report review workflow (approve/reject)
- Notification model with read/unread tracking
- Console email backend for local development

## Tech stack

- Python
- Django 5.2
- SQLite (default development database)
- Pillow for image uploads

## Requirements

- Python 3.11+ recommended
- `pip` package manager

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd daily_reporting_system_django
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Collect static files (optional for production):

```bash
python manage.py collectstatic
```

## Environment variables

The project supports the following environment variables:

- `DJANGO_SECRET_KEY` — secret key for Django
- `DJANGO_DEBUG` — enable/disable debug mode (`True` or `False`)
- `DJANGO_ALLOWED_HOSTS` — comma-separated list of allowed hosts

If not provided, defaults are used for local development.

## Running locally

Start the development server:

```bash
python manage.py runserver
```

Open the site at `http://127.0.0.1:8000/`.

## URL endpoints

- `/` — dashboard (redirects to login if unauthenticated)
- `/login/` — user login
- `/register/` — user registration
- `/logout/` — logout
- `/profile/` — profile management
- `/change-password/` — password change
- `/forget-password/` — password reset request
- `/tasks/` — task listing
- `/tasks/create/` — create a new task (admin/manager only)
- `/tasks/my-tasks/` — tasks assigned to current user
- `/reports/submit/` — submit a daily report
- `/reports/my-reports/` — view own reports
- `/reports/all/` — view all reports (admin/manager only)
- `/notifications/` — notification inbox

## Application structure

- `accounts/` — custom user model, authentication, registration, profile, dashboard
- `tasks/` — task assignment and progress tracking
- `reports/` — daily report submission and review
- `notifications/` — notification generation and listing
- `core/` — project settings, URL configuration, WSGI/ASGI entrypoints

## Database

The default database is SQLite and uses `db.sqlite3` in the project root.

## Testing

Run tests with:

```bash
python manage.py test
```

## Notes

- The project uses `django.core.mail.backends.console.EmailBackend` for local email handling.
- Uploaded media files are stored in the `media/` directory during development.
- Static assets are served from `static/` and `staticfiles/` in development when `DEBUG=True`.

## Recommended additions

For production deployment, consider:

- switching to PostgreSQL or another production-ready database
- setting `DJANGO_DEBUG=False`
- using a real email backend
- configuring static/media hosting
- securing secret key and environment variables

## License

This repository does not include a license file by default. Add one if you plan to open source the project.
