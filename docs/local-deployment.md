# Run and test the portfolio locally

Updated 2026-10-20. These instructions use PowerShell on Windows and the current Flask application.

## 1. Open the project

Open a VS Code terminal and run:

```powershell
Set-Location -LiteralPath 'C:\Users\verla\OneDrive\Desktop\Projects\portfolio'
py -3.13 --version
```

Python 3.13 is required. If the Python launcher is unavailable, use an installed Python 3.13 executable instead of `py -3.13`.

The new site starts from `app.py`. Opening `index.htm` or using an HTML-only Live Server shows the legacy site and cannot render Flask/Jinja pages.

## 2. Set up dependencies

On a fresh checkout, create the virtual environment:

```powershell
py -3.13 -m venv .venv
```

If `.venv` already exists and uses Python 3.13, reuse it. Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Using the environment's executable directly avoids PowerShell activation-policy changes. There is no npm install, database, frontend build, or secret configuration needed to run the site.

## 3. Start the local server

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

Keep this terminal open. Visit **http://127.0.0.1:5000/**.

This is a local development preview, not an always-on production server. Binding to `127.0.0.1` makes it accessible on this computer. It does not publish the site to the internet.

If a preview is already running on port 5000, use that one. To run another:

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5001 --no-debugger --no-reload
```

Then visit http://127.0.0.1:5001/.

## 4. Test the site

Check these pages in the browser:

| Page | Local path | Check |
| --- | --- | --- |
| Home | `/` | Hero, project link, experience previews |
| About | `/about/` | Biography and navigation |
| Experience | `/experience/` | Four résumé-sourced employer entries |
| Projects | `/projects/` | Search `Flask`, select a category, try a term with no matches |
| Project detail | `/projects/personal-portfolio/` | Case study and repository link |
| Resume | `/resume/` | Download opens the supplied two-page PDF |
| Contact | `/contact/` | LinkedIn, GitHub, email |
| Missing page | `/not-a-page/` | Styled 404 |

Try a narrow browser window, keyboard Tab/Enter, the skip link, and the mobile menu. Escape should close the menu and return focus to its button.

Run automated checks in a second terminal at the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The current suite has 26 passing tests. If Node is installed, also check JavaScript:

```powershell
Get-Content public/js/main.js | node --input-type=module --check
Get-Content public/js/navigation.js | node --input-type=module --check
```

## 5. Make changes and restart

- Content: edit approved JSON in `data/`.
- Page structure: edit `templates/`.
- Styling: edit `public/css/`.
- Behavior: edit `public/js/`.

With reloading disabled, stop and restart Flask after Python, JSON, or template changes. Refresh the browser after CSS/JavaScript changes; use Ctrl+F5 if cached assets remain.

To stop the server, press **Ctrl+C in its terminal**. Restart with the command from step 3.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `No module named flask` | Use `.venv\Scripts\python.exe`; install requirements into that environment |
| Port is already in use | Use the running preview or switch to port 5001 |
| Legacy page appears | Open the Flask URL, not `index.htm` or Live Server |
| CSS/JS return 404 locally | Check whether the shell has `VERCEL` set; it disables local asset routes |
| `SITE_URL` validation error | Leave it unset locally; it accepts only an HTTPS origin without a path |
| Old content remains | Restart Flask; JSON is loaded at application startup |
| Résumé unavailable | Check `public/resume.pdf` and `resume_approved` in `data/profile.json` |

For a shell reused from Vercel tooling, clear only these process-level deployment variables before restarting:

```powershell
Remove-Item Env:VERCEL, Env:VERCEL_ENV, Env:SITE_URL -ErrorAction SilentlyContinue
```

Local responses intentionally use noindex. This is expected.

## Bash equivalent

From the project directory on a system with Python 3.13:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m flask --app app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

For hosted deployment, continue with [Vercel deployment](vercel-deployment.md).
