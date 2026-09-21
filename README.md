# Restituo

3D archaeological restitution site and client request management platform,
hosted at sagalhaider.com. End-of-year project, Holberton School Paris —
Cybersecurity Software Engineering (RNCP level 6).

This document covers installation, the development environment (CP1) and
deployment (CP8).

## Tech stack

| Area | Choice |
| --- | --- |
| Backend | Django 5.2 |
| Database (SQL) | SQLite locally, PostgreSQL in production, via the Django ORM |
| Key-value store (NoSQL) | Redis, used for rate limiting on `/demandes`, `/chatbot/message` and `/login` |
| Frontend | Django templates (server-rendered) |
| Admin auth | Native Django sessions |
| Chatbot | FAQ rules (`ChatbotRule`) falling back to the Anthropic API |
| Email | SMTP (Gmail) |
| Tests | pytest-django |
| CI/CD | GitHub Actions |
| Hosting | VPS (nginx + gunicorn) |

The full mapping to the RNCP competencies (CP1 to CP8) is in
`docs/RNCP-MAPPING.md`.

## CP1 — Set up and configure the development environment

### Requirements

- Python 3.11+
- Redis (optional locally, see below)

### Installation

```bash
git clone git@github.com:sagalou/sagalhaider-com.git
cd sagalhaider-com
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` if needed (Anthropic key, SMTP credentials...). By default:
- SQLite as the database
- `REDIS_DISABLED=1`: rate limiting uses local memory instead of Redis, so
  you don't need to run a Redis server in dev
- emails are just printed to the terminal (`console` backend)

### Run the project

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_realisations initial_rules  # demo content
python manage.py runserver
```

The site is at http://127.0.0.1:8000, the Django admin at
http://127.0.0.1:8000/django-admin/, and the client dashboard login at
http://127.0.0.1:8000/login.

### Run the tests

```bash
pytest
```

### With Redis locally (optional)

```bash
docker run -p 6379:6379 redis:7-alpine
# then in .env: REDIS_DISABLED=0
```

## Project structure

```
config/            Django settings, root urls
core/               public pages (home, sites, cities, contact)
realisations/       Realisation model + /realisations endpoint
servicerequests/    ServiceRequest, RequestStep, client form, admin dashboard
chatbot/            ChatbotRule, ChatbotService, /chatbot/message endpoint
accounts/           admin login/logout
core/ratelimit.py   Redis-backed rate limiting (NoSQL component, CP6)
templates/          Django templates
static/             CSS, JS
portfolio/           static CV page, outside the RNCP project's scope
```

## Endpoints

See the detailed table in the technical documentation (Stage 3). Summary:

| Endpoint | Method | Auth |
| --- | --- | --- |
| `/realisations` | GET | no |
| `/demandes` | POST | no (rate limited) |
| `/login` | GET/POST | no |
| `/admin/dashboard` | GET | yes (session) |
| `/admin/demandes` | GET | yes (session) |
| `/admin/demandes/{id}` | GET | yes (session) |
| `/admin/demandes/{id}/etapes/{step_id}/complete` | POST | yes (session) |
| `/chatbot/message` | POST | no (rate limited) |

## CP8 — Deployment documentation

### Infrastructure

- Ubuntu 24.04 VPS (hosted by Hugo Chilemme)
- nginx as reverse proxy + basic WAF (rate limiting, basic rules)
- gunicorn as the WSGI server, run via a systemd service
- PostgreSQL as the production database
- Redis for rate limiting

### Deployment (automatic CI/CD)

Deployment is handled by `.github/workflows/ci.yml`:

1. On every push/PR: the `pytest` suite runs against a real Redis service
   container.
2. On a push to `main`, **if tests pass**: the code is synced to the VPS
   over SSH via `rsync`, migrations are applied, static files are
   collected, and the gunicorn service is restarted.

GitHub secrets to configure in the repo (`Settings > Secrets and
variables > Actions`):

- `VPS_SSH_KEY`: SSH private key used for deployment
- `VPS_HOST`: VPS address
- `VPS_USER`: SSH user
- `VPS_PORT`: SSH port (2006, alias `safa`)

### Manual deployment (first-time setup on the VPS)

```bash
ssh safa   # SSH alias configured locally, port 2006
sudo mkdir -p /var/www/sagalhaider-com
sudo chown $USER:$USER /var/www/sagalhaider-com
cd /var/www/sagalhaider-com
git clone git@github.com:sagalou/sagalhaider-com.git .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit with real production values
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

`systemd` unit file (`/etc/systemd/system/sagalhaider-gunicorn.service`):

```ini
[Unit]
Description=gunicorn daemon for sagalhaider.com
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/sagalhaider-com
ExecStart=/var/www/sagalhaider-com/venv/bin/gunicorn config.wsgi:application \
    --bind 127.0.0.1:8001 --workers 3
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

nginx block (excerpt, adapt in `/etc/nginx/sites-available/sagalhaider.com`):

```nginx
limit_req_zone $binary_remote_addr zone=sagalhaider:10m rate=10r/s;

server {
    server_name sagalhaider.com;

    location / {
        limit_req zone=sagalhaider burst=20 nodelay;
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ { alias /var/www/sagalhaider-com/staticfiles/; }
    location /media/  { alias /var/www/sagalhaider-com/media/; }
    location /portfolio/ { alias /var/www/sagalhaider-com/portfolio/; }
}
```

### Rollback

If a deployment breaks: `git checkout <previous commit>` on the VPS, then
`python manage.py migrate` (watch out for irreversible migrations) and
`sudo systemctl restart sagalhaider-gunicorn`.

## Git workflow

- `dev` branch and feature branches (`feature/xxx`)
- Pull request with self-review before merging into `main`
- `main` is the branch deployed automatically