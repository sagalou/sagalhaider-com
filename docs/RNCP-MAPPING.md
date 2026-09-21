# Mapping RNCP 5 — Activités & Compétences

Référence : fiche RNCP niveau 5, activités types 1 et 2 (développer le
front-end et le back-end d'une application web sécurisée).

## Activité type 1 — Développer la partie front-end

| CP | Compétence | Où c'est fait dans le projet |
| --- | --- | --- |
| CP1 | Installer et configurer son environnement de travail | `README.md` (installation, `.env.example`), `requirements.txt`, structure du repo |
| CP2 | Maquetter des interfaces utilisateur web ou web mobile | Wireframes/maquettes à ajouter dans `docs/maquettes/` (Figma) — reprend la structure visuelle existante : accueil, galerie, formulaire, dashboard admin |
| CP3 | Réaliser des interfaces utilisateur statiques web ou web mobile | `templates/` (HTML sémantique) + `static/css/style.css`, responsive (media queries) |
| CP4 | Développer la partie dynamique des interfaces utilisateur | `static/js/chatbot.js` (widget chatbot, fetch API), `templates/core/contact.html` (soumission AJAX du formulaire), `templates/servicerequests/dashboard.html` (dashboard entièrement piloté en JS via fetch) |

## Activité type 2 — Développer la partie back-end

| CP | Compétence | Où c'est fait dans le projet |
| --- | --- | --- |
| CP5 | Mettre en place une base de données relationnelle | Modèles Django (`realisations/models.py`, `servicerequests/models.py`, `chatbot/models.py`), migrations dans chaque app |
| CP6 | Développer des composants d'accès aux données SQL et NoSQL | SQL : ORM Django partout (requêtes paramétrées par construction). NoSQL : `core/ratelimit.py`, backend Redis (`django-redis`), utilisé par `/demandes`, `/chatbot/message` et `/login` pour le rate limiting |
| CP7 | Développer des composants métier côté serveur | Endpoints REST (`*/views.py` de chaque app), logique métier dans les modèles (`ServiceRequest.send_confirmation()`, `check_response_delay()`, `progress()`), `ChatbotService` |
| CP8 | Documenter le déploiement d'une application dynamique web ou web mobile | `README.md` section CP8, `.github/workflows/ci.yml` (CI/CD) |

## Sécurité (transversal au titre "sécurisée")

- Injection SQL : ORM Django (requêtes paramétrées)
- Mots de passe : hashage natif Django (PBKDF2)
- CSRF : protection Django activée partout sauf les endpoints publics
  explicitement anonymes (`/demandes`, `/chatbot/message`), qui sont eux
  protégés par rate limiting au lieu du CSRF (pas de session à protéger)
- Anti-spam : honeypot sur le formulaire de demande (`servicerequests/forms.py`)
- Rate limiting : sur les 3 endpoints publics les plus exposés (`/demandes`,
  `/chatbot/message`, `/login`)
- WAF : règles nginx (rate limiting, voir `README.md`)
- Secrets : hors du repo, via `.env` (jamais commité, voir `.gitignore`)

## Ce qui reste à faire pour un dossier complet

- [ ] Ajouter les maquettes Figma dans `docs/maquettes/` (CP2)
- [ ] Ajouter du contenu réel dans `Realisation` (au moins Beta Samati)
      via l'admin, avec vraies images/vidéos
- [ ] Configurer les vrais secrets GitHub Actions pour le déploiement
- [ ] Ajouter Argon2 comme hasher (mentionné comme amélioration possible
      dans la doc technique)
- [ ] Mettre à jour le document Notion technique pour y ajouter Redis/NoSQL
      (actuellement absent, ajouté ici suite à la relecture RNCP)
