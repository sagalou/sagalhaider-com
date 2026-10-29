# Retrospectives

As a solo developer, I held the retrospective alone at the end of each sprint, with three questions: what worked, what was hard, what I change for the next sprint.

## Sprint 1 (September 21 to 27)
**What worked:** the Stage 3 documentation made the backend structure clear, so the five Django apps were quick to set up.

**What was hard:** the whole backend went into one large commit and one pull request, which is hard to review and to roll back.

**Next sprint:** smaller commits, one feature per branch.

## Sprint 2 (September 28 to October 4)
**What worked:** a lot of features delivered, and a full security hardening pass.

**What was hard:**
- CSRF errors in production only, because Chilemme's proxy terminates HTTPS before Django. Fixed by trusting the proxy headers.
- Cloudflare kept serving old CSS and JS files. Fixed with a version query parameter.
- Most commits went straight to `dev` without pull requests.

**Next sprint:** every change goes through a feature branch and a pull request; adopt a commit message convention (`feat:`, `fix:`, `docs:`, `style:`, `ci:`).

## Sprint 3 (October 5 to 11)
**What worked:** pull requests for every change, linters in the CI, consistent commit messages.

**What was hard:** the production terminal (Chilemme's web terminal) does not behave like my local terminal: no `sudo`, no `source venv/bin/activate`, commands one at a time. I made the same mistakes several times.

**Next sprint:** keep a written deployment reference sheet with the exact production commands.

## Sprint 4 (October 12 to 18)
**What worked:** reviewing my own code with a security point of view found a real stored XSS in the dashboard, fixed before release.

**What was hard:** the XSS came from inserting client data with `innerHTML`; it worked, so I had not seen the risk.

**Next sprint:** escape all user data by default in the front end; check the production result after each security change (Argon2 hash verified in the production shell).

## Sprint 5 (October 19 to 28)
**What worked:** the codebase is documented and the release on `main` is clean.

**What was hard:** keeping the documentation consistent with the code (the docs mentioned PostgreSQL in production while production runs SQLite).

**Next steps:** after the MVP, calendar integration in the dashboard, and PostgreSQL if traffic grows.
