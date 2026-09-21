# RNCP 5 Mapping — Activities & Competencies

Reference: RNCP level 5 record, activity types 1 and 2 (developing the
front-end and back-end of a secured web application).

## Activity type 1 — Develop the front-end

| CP | Competency | Where it's done in the project |
| --- | --- | --- |
| CP1 | Install and configure the development environment | `README.md` (installation, `.env.example`), `requirements.txt`, repo structure |
| CP2 | Wireframe/mock up web or mobile web user interfaces | Wireframes/mockups to add in `docs/mockups/` (Figma) — should mirror the existing visual structure: home, gallery, form, admin dashboard |
| CP3 | Build static web or mobile web user interfaces | `templates/` (semantic HTML) + `static/css/style.css`, responsive (media queries) |
| CP4 | Develop the dynamic part of user interfaces | `static/js/chatbot.js` (chatbot widget, fetch API), `templates/core/contact.html` (AJAX form submission), `templates/servicerequests/dashboard.html` (dashboard entirely driven by JS via fetch) |

## Activity type 2 — Develop the back-end

| CP | Competency | Where it's done in the project |
| --- | --- | --- |
| CP5 | Set up a relational database | Django models (`realisations/models.py`, `servicerequests/models.py`, `chatbot/models.py`), migrations in each app |
| CP6 | Develop SQL and NoSQL data access components | SQL: Django ORM throughout (parameterized queries by construction). NoSQL: `core/ratelimit.py`, Redis backend (`django-redis`), used by `/demandes`, `/chatbot/message` and `/login` for rate limiting |
| CP7 | Develop server-side business components | REST endpoints (`*/views.py` in each app), business logic in the models (`ServiceRequest.send_confirmation()`, `check_response_delay()`, `progress()`), `ChatbotService` |
| CP8 | Document the deployment of a dynamic web or mobile web application | `README.md` CP8 section, `.github/workflows/ci.yml` (CI/CD) |

## Security (cross-cutting, covers the "secured" part of the title)

- SQL injection: Django ORM (parameterized queries)
- Passwords: Django's native hashing (PBKDF2)
- CSRF: Django protection enabled everywhere except the public endpoints
  that are explicitly anonymous (`/demandes`, `/chatbot/message`), which
  are protected by rate limiting instead of CSRF (no session to protect)
- Anti-spam: honeypot field on the request form (`servicerequests/forms.py`)
- Rate limiting: on the 3 most exposed public endpoints (`/demandes`,
  `/chatbot/message`, `/login`)
- WAF: nginx rules (rate limiting, see `README.md`)
- Secrets: kept out of the repo, via `.env` (never committed, see `.gitignore`)

## What's left for a complete submission

- [ ] Add Figma mockups to `docs/mockups/` (CP2)
- [ ] Add real content to `Realisation` (at least Beta Samati) via the
      admin, with real images/videos
- [ ] Configure real GitHub Actions secrets for deployment
- [ ] Add Argon2 as the password hasher (mentioned as a possible
      improvement in the technical documentation)
- [ ] Update the Notion technical document to add Redis/NoSQL (currently
      missing, added here following the RNCP review)