# Sprint Planning

Restituo is a solo project. I held every role: Project Manager, Source Control Manager, QA and Developer.

- **Sprint length:** 1 week
- **Tools:** GitHub (feature branches, pull requests, Issues), GitHub Actions (lint and tests on every push)
- **Branching:** `feature/*`, `fix/*` and `docs/*` branches merged into `dev` through pull requests; `dev` is deployed to the VPS; `dev` is merged into `main` for releases

## MoSCoW prioritization

| Priority | Features |
|---|---|
| **Must have** | Public gallery of 3D restitutions, public service request form, admin dashboard to follow requests, authentication with 2FA, chatbot with FAQ, production deployment |
| **Should have** | LLM fallback for the chatbot, FR/EN/SW translations, 7-day reminder for unanswered requests, progress tracking per request |
| **Could have** | Videos in the gallery, About page, accessibility improvements (RGAA) |
| **Won't have (this MVP)** | Client accounts, calendar integration in the dashboard, PostgreSQL (SQLite is enough at this scale) |

## Dependencies

1. The Django backend (Sprint 1) is required before any feature.
2. Admin authentication and 2FA must exist before the dashboard is exposed.
3. Security hardening and code style must be done before the security audit (Sprint 4).
4. All features must be merged before the final documentation and release (Sprint 5).

## Sprints

### Sprint 0 (August 31)
**Goal:** start from the existing static site.

| Task | Owner | Status |
|---|---|---|
| Import the existing static site | Sagal | Done |
| Separate HTML, CSS and JS into folders | Sagal | Done |

*September 1 to 20: Stages 2 and 3 (technical documentation), no code.*

### Sprint 1 (September 21 to 27)
**Goal:** build the Django backend.

| Task | Owner | Deadline | Status |
|---|---|---|---|
| Django project with apps: core, accounts, servicerequests, chatbot, realisations | Sagal | Sept 27 | Done |
| Models, forms and views for service requests | Sagal | Sept 27 | Done |
| Fix dashboard text contrast | Sagal | Sept 27 | Done |
| Rename the project to Restituo, translate docs to English | Sagal | Sept 27 | Done |

### Sprint 2 (September 28 to October 4)
**Goal:** content, translations and security hardening.

| Task | Owner | Deadline | Status |
|---|---|---|---|
| Video field on Realisation, with real MIME type validation | Sagal | Oct 4 | Done |
| EN/SW translations | Sagal | Oct 4 | Done |
| New color palette and homepage copy | Sagal | Oct 4 | Done |
| Chatbot widget: attention bubble, welcome message | Sagal | Oct 4 | Done |
| HSTS, secure cookies, SSL redirect, django-axes | Sagal | Oct 4 | Done |
| Security logging, SQLite backup script | Sagal | Oct 4 | Done |
| 2FA (TOTP) on the Django admin | Sagal | Oct 4 | Done |
| Calendar integration in the dashboard | Sagal | Oct 4 | Moved to Won't have |

### Sprint 3 (October 5 to 11)
**Goal:** code quality and continuous integration.

| Task | Owner | Deadline | Status |
|---|---|---|---|
| pycodestyle and pydocstyle compliance | Sagal | Oct 11 | Done |
| Lint step in GitHub Actions before tests | Sagal | Oct 11 | Done |
| Move chatbot inline styles to CSS | Sagal | Oct 11 | Done |
| `CHATBOT_MODEL_TIER` switch (low/high model) | Sagal | Oct 11 | Done |
| Require 2FA on the admin dashboard and its API | Sagal | Oct 11 | Done |

### Sprint 4 (October 12 to 18)
**Goal:** security audit and remaining features.

| Task | Owner | Deadline | Status |
|---|---|---|---|
| Fix stored XSS in the dashboard | Sagal | Oct 18 | Done |
| Argon2 password hashing (PBKDF2 kept as fallback) | Sagal | Oct 18 | Done |
| Chatbot UI translations | Sagal | Oct 18 | Done |
| `send_reminders` command (7-day reminder) | Sagal | Oct 18 | Done |
| About page | Sagal | Oct 18 | Done |
| Accessibility fixes (RGAA) | Sagal | Oct 18 | Done |

### Sprint 5 (October 19 to 28)
**Goal:** documentation and release.

| Task | Owner | Deadline | Status |
|---|---|---|---|
| Document SQLite in production | Sagal | Oct 28 | Done |
| Clean README | Sagal | Oct 28 | Done |
| Comment JS files and templates | Sagal | Oct 28 | Done |
| Remove duplicate route and outdated copy | Sagal | Oct 28 | Done |
| Merge `dev` into `main` | Sagal | Oct 28 | Done |
| GDPR privacy page and log retention | Sagal | Oct 28 | Done |
| Protect server-only folders in the deploy workflow | Sagal | Oct 28 | Done |

## Metrics

| Sprint | Planned | Completed | Completion |
|---|---|---|---|
| 1 | 4 | 4 | 100% |
| 2 | 8 | 7 | 88% (calendar postponed) |
| 3 | 5 | 5 | 100% |
| 4 | 6 | 6 | 100% |
| 5 | 7 | 7 | 100% |

Average velocity: about 6 tasks per sprint.
