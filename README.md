# Luigi Josue — personal portfolio

Flask/Jinja, Bootstrap 5, custom CSS, and vanilla JavaScript. Public professional experience and personal technical work. No database or frontend build step.

Step-by-step guides: [local setup and testing](docs/local-deployment.md) · [Vercel preview, production, and Git deployment](docs/vercel-deployment.md).

## Run locally

Python 3.13 is required. From the repository in PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m flask --app app run --port 5000
```

Open `http://127.0.0.1:5000/`. On Bash, create the same environment with `python3.13 -m venv .venv` and use `.venv/bin/python` for the remaining commands.

## Check and prepare

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/stage_release.py
```

Staging creates a local allowlisted package and hash manifest under `.release/`. It does not deploy. Inspect it before upload.

GitHub Actions runs the tests, JavaScript syntax checks, and staging on development-branch pushes and pull requests. It has read-only repository permissions and no deployment steps. See the [release review](docs/release-review.md) for the next approval and preview procedure.

## Maintain

- `data/`: approved profile, experience, skills, and public projects.
- `templates/`: shared Jinja layouts and pages.
- `public/css/`: local fonts, tokens, layout, Bootstrap customization.
- `public/js/`: small progressive navigation module.
- `public/vendor/`: Bootstrap CSS and license.
- `tests/`: application, HTML, link, mount-path, and staging checks.
- `docs/`: architecture, plan, content evidence, deployment notes, QA.

Employment follows the user-supplied public résumé, received 2026-10-20. Its unchanged PDF is available at `public/resume.pdf`; approval and SHA-256 are recorded in `data/profile.json`. Review any replacement, update the hash, and rerun tests before publication. Do not store unpublished or confidential material anywhere in `public/` or `data/`.

The existing GitHub Pages source (`index.htm`, `stylesheets/`) remains unchanged. Flask requires a Python host and cannot execute on Pages. Intended host: Vercel, subject to content review, preview validation, and release approval. See [deployment](docs/deployment.md) and [implementation plan](docs/implementation-plan.md).
