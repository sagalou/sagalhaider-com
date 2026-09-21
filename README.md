# sagalhaider.com

Site de restitution 3D archéologique et plateforme de gestion de demandes
clients. Projet de fin d'année, Holberton School Paris — Cybersecurity
Software Engineering (RNCP niveau 6).

Ce document couvre l'installation, l'environnement de travail (CP1) et le
déploiement (CP8).

## Stack technique

| Domaine | Choix |
| --- | --- |
| Backend | Django 5.2 |
| Base de données (SQL) | SQLite en local, PostgreSQL en production, via l'ORM Django |
| Base clé-valeur (NoSQL) | Redis, pour le rate limiting sur `/demandes`, `/chatbot/message` et `/login` |
| Frontend | Templates Django (rendu serveur) |
| Auth admin | Sessions Django natives |
| Chatbot | Règles FAQ (`ChatbotRule`) en fallback vers l'API Anthropic |
| Email | SMTP (Gmail) |
| Tests | pytest-django |
| CI/CD | GitHub Actions |
| Hébergement | VPS (nginx + gunicorn) |

Le mapping complet avec les compétences RNCP (CP1 à CP8) est dans
`docs/RNCP-MAPPING.md`.

## CP1 — Installer et configurer son environnement de travail

### Prérequis

- Python 3.11+
- Redis (optionnel en local, voir plus bas)

### Installation

```bash
git clone git@github.com:sagalou/sagalhaider-com.git
cd sagalhaider-com
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Éditer `.env` si besoin (clé Anthropic, identifiants SMTP...). Par défaut :
- SQLite en base
- `REDIS_DISABLED=1` : le rate limiting utilise la mémoire locale au lieu
  de Redis, pour ne pas avoir à lancer un serveur Redis en dev
- les emails sont juste affichés dans le terminal (`console` backend)

### Lancer le projet

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_realisations initial_rules  # contenu de démo
python manage.py runserver
```

Le site est sur http://127.0.0.1:8000, l'admin Django sur
http://127.0.0.1:8000/django-admin/, et le dashboard client sur
http://127.0.0.1:8000/login.

### Lancer les tests

```bash
pytest
```

### Avec Redis en local (optionnel)

```bash
docker run -p 6379:6379 redis:7-alpine
# puis dans .env : REDIS_DISABLED=0
```

## Structure du projet

```
config/            réglages Django, urls racine
core/               pages publiques (accueil, sites, villes, contact)
realisations/       modèle Realisation + endpoint /realisations
servicerequests/    ServiceRequest, RequestStep, formulaire client, dashboard admin
chatbot/            ChatbotRule, ChatbotService, endpoint /chatbot/message
accounts/           connexion/déconnexion admin
core/ratelimit.py   rate limiting basé sur Redis (composant NoSQL, CP6)
templates/          templates Django
static/             CSS, JS
portfolio/           page CV statique, hors périmètre du projet RNCP
```

## Endpoints

Voir le tableau détaillé dans la documentation technique (Stage 3). Résumé :

| Endpoint | Méthode | Auth |
| --- | --- | --- |
| `/realisations` | GET | non |
| `/demandes` | POST | non (rate limité) |
| `/login` | GET/POST | non |
| `/admin/dashboard` | GET | oui (session) |
| `/admin/demandes` | GET | oui (session) |
| `/admin/demandes/{id}` | GET | oui (session) |
| `/admin/demandes/{id}/etapes/{step_id}/complete` | POST | oui (session) |
| `/chatbot/message` | POST | non (rate limité) |

## CP8 — Documentation du déploiement

### Infrastructure

- VPS Ubuntu 24.04 (hébergé par Hugo Chilemme)
- nginx en reverse proxy + WAF basique (rate limiting, règles de base)
- gunicorn comme serveur WSGI, lancé via un service systemd
- PostgreSQL en base de données de production
- Redis pour le rate limiting

### Déploiement (CI/CD automatique)

Le déploiement est géré par `.github/workflows/ci.yml` :

1. Sur chaque push/PR : les tests `pytest` tournent avec un vrai Redis en
   service Docker.
2. Sur un push sur `main` **si les tests passent** : le code est envoyé
   sur le VPS par `rsync` en SSH, les migrations sont appliquées, les
   fichiers statiques sont collectés, et le service gunicorn est redémarré.

Secrets GitHub à configurer dans le repo (`Settings > Secrets and
variables > Actions`) :

- `VPS_SSH_KEY` : clé privée SSH de déploiement
- `VPS_HOST` : adresse du VPS
- `VPS_USER` : utilisateur SSH
- `VPS_PORT` : port SSH (2006, alias `safa`)

### Déploiement manuel (première installation sur le VPS)

```bash
ssh safa   # alias SSH configuré en local, port 2006
sudo mkdir -p /var/www/sagalhaider-com
sudo chown $USER:$USER /var/www/sagalhaider-com
cd /var/www/sagalhaider-com
git clone git@github.com:sagalou/sagalhaider-com.git .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # puis éditer avec les vraies valeurs de prod
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Fichier `systemd` (`/etc/systemd/system/sagalhaider-gunicorn.service`) :

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

Bloc nginx (extrait, à adapter dans `/etc/nginx/sites-available/sagalhaider.com`) :

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

En cas de déploiement cassé : `git checkout <commit précédent>` sur le
VPS, puis `python manage.py migrate` (attention aux migrations
irréversibles) et `sudo systemctl restart sagalhaider-gunicorn`.

## Workflow Git

- Branches `dev` et branches de fonctionnalité (`feature/xxx`)
- Pull request avec auto-review avant fusion dans `main`
- `main` est la branche déployée automatiquement
