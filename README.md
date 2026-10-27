# Restituo

3D archaeological restitution site and client request management platform,
hosted at sagalhaider.com.

## Tech stack

| Area | Choice |
| --- | --- |
| Backend | Django 5.2 |
| Database | SQLite, via the Django ORM |
| Rate limiting | Redis (optional locally) |
| Frontend | Django templates |
| Chatbot | FAQ rules with an LLM fallback (Mistral API) |
| Tests | pytest-django |
| CI | GitHub Actions |

## Requirements

- Python 3.11+
- Redis (optional, see below)

## Installation

```bash
git clone git@github.com:sagalou/sagalhaider-com.git
cd sagalhaider-com
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` if needed (API key, SMTP credentials). By default:

- SQLite is used as the database
- `REDIS_DISABLED=1`: rate limiting uses local memory, no Redis server needed
- emails are printed to the terminal

## Run the project

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_realisations initial_rules
python manage.py runserver
```

- Site: http://127.0.0.1:8000
- Django admin: http://127.0.0.1:8000/django-admin/
- Dashboard login: http://127.0.0.1:8000/login

## Run the tests

```bash
pytest
```

## With Redis (optional)

```bash
docker run -p 6379:6379 redis:7-alpine
```

Then set `REDIS_DISABLED=0` in `.env`.
