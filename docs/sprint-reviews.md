# Sprint Reviews

At the end of each sprint, I checked the delivered features on the deployed site (sagalhaider.com) and compared them with the sprint goal.

## Sprint 1 (September 21 to 27)
**Goal:** build the Django backend.

**Demo:**
- The Django backend runs with its five apps and replaces the static site.
- A visitor can submit a service request through the public form, and it is saved in the database.
- The project is renamed Restituo and the documentation is in English.

**Result:** goal reached. Merged through PR #1.

## Sprint 2 (September 28 to October 4)
**Goal:** content, translations and security hardening.

**Demo:**
- The gallery shows videos of the 3D restitutions.
- The site is available in French, English and Swahili.
- New visual identity (stone and patina green).
- The chatbot widget welcomes visitors.
- Security: HTTPS enforced (HSTS, SSL redirect, secure cookies), brute force protection with django-axes, uploaded videos checked by their real MIME type, security events logged, daily SQLite backups, 2FA on the Django admin.

**Result:** goal reached, except the calendar integration in the dashboard, moved out of the MVP.

## Sprint 3 (October 5 to 11)
**Goal:** code quality and continuous integration.

**Demo:**
- Python code follows pycodestyle and pydocstyle.
- GitHub Actions runs the linters, then the tests, on every push.
- The chatbot model can be switched with an environment variable (cheap model for tests, better model for demos).
- The admin dashboard and its API now require a session validated with 2FA.

**Result:** goal reached. Merged through PRs #2 to #6.

## Sprint 4 (October 12 to 18)
**Goal:** security audit and remaining features.

**Demo:**
- Client data is escaped before display in the dashboard (stored XSS fixed).
- Passwords are hashed with Argon2; the hash in production starts with `argon2$argon2id$`.
- The chatbot interface is translated.
- The admin receives an email when a request has been waiting for more than 7 days.
- New About page.
- Accessibility: keyboard navigation, form labels, contrast, landmarks.

**Result:** goal reached. Merged through PRs #7 and #8.

## Sprint 5 (October 19 to 28)
**Goal:** documentation and release.

**Demo:**
- Clean README, comments in every JS file and template.
- `dev` merged into `main` (PR #9 and #10).
- GDPR privacy page, notice on the form, log retention.

**Result:** goal reached. The MVP is live on sagalhaider.com.
