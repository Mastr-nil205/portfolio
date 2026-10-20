# Deploy the portfolio to Vercel

Updated 2026-10-20 against official documentation. This is a procedure to follow when deployment is approved; writing this guide did not create a project, upload files, or deploy.

Start with a CLI preview of the reviewed release package. Configure production and Git integration separately after that preview passes.

## 1. Prerequisites and scope

- Complete [local setup and tests](local-deployment.md).
- Have a Vercel account and Node/npm available for its CLI.
- Review the public content, including the résumé's email and phone.
- Keep private drafts outside the repository.
- Review [Hobby restrictions](https://vercel.com/docs/plans/hobby). The plan is for personal, non-commercial use with usage limits; removing business sections alone does not guarantee eligibility.

Use the default `.vercel.app` domain. No custom domain, database, or paid service is needed for the proposed setup.

The existing GitHub Pages site stays separate. Do not merge this branch into `master` while Pages selects `master:/docs`; that configuration must be addressed separately before any such merge.

## 2. Test and stage an exact upload

Run from the repository root in PowerShell:

```powershell
Set-Location -LiteralPath 'C:\Users\verla\OneDrive\Desktop\Projects\portfolio'
.\.venv\Scripts\python.exe -m pytest -q
```

Stop if tests fail. When they pass:

```powershell
$releasePath = .\.venv\Scripts\python.exe scripts/stage_release.py
if ($LASTEXITCODE -ne 0) { throw 'Release staging failed.' }
Get-ChildItem -LiteralPath $releasePath -Force
```

The script prints a new timestamped directory under `.release/` and writes an adjacent SHA-256 manifest. Review that exact directory. It includes the application, approved JSON, templates, public assets, and runtime configuration. It excludes the legacy site, docs, tests, virtual environment, and review caches.

Record the source revision:

```powershell
git rev-parse HEAD
git status --short
```

If files are modified, review and commit intended changes before associating a release with a commit. Never assume a working-directory package exactly matches HEAD when there are uncommitted changes.

## 3. Sign in and link the staged directory

The following commands use the official Vercel CLI via npm; they do not add a JavaScript framework to the application:

```powershell
npx vercel@latest login
Set-Location -LiteralPath $releasePath
npx vercel@latest link
```

Complete sign-in in your browser. Select your intended account/scope and create or select the portfolio project. Use a recognizable project name, such as `luigi-josue-portfolio`, rather than the staging timestamp. Confirm the selected directory is the staged package.

`link` associates this directory with a project and writes local `.vercel` metadata. Do not commit credentials or project-link metadata. Each newly staged directory must be linked to the **same existing project** on subsequent releases. [CLI linking](https://vercel.com/docs/cli/link).

## 4. Confirm project settings

| Setting | Value |
| --- | --- |
| Framework | Flask / automatic Flask detection |
| Root directory | The staged directory for CLI; repository root (`.`) for Git integration |
| Python | 3.13, specified by `.python-version` and `pyproject.toml` |
| Entrypoint | `app.py` exporting `app`; also declared as `app:app` |
| Install command | Use automatic Python dependency installation |
| Build command | Leave the framework default; no npm build |
| Output directory | Leave the framework default; do not set `public` as a static-only output |

Vercel runs Flask as a function and serves `public/` assets from its CDN. This repository already includes `vercel.json` and `.vercelignore`. Do not replace them with an unrelated legacy Python routing example. [Official Flask guide](https://vercel.com/docs/frameworks/backend/flask).

Leave `SITE_URL` unset for the first preview. Vercel supplies its platform variables; verify automatic system-variable exposure is enabled if those values are missing. Do not manually force `VERCEL_ENV=production` for a preview.

## 5. Deploy a preview

From the linked staged directory:

```powershell
npx vercel@latest deploy --target=preview
```

**This command uploads the staged files to Vercel.** Copy the returned deployment URL and confirm its environment is Preview in the dashboard. Inspect build logs if it fails. The explicit target selects the preview environment. [Deploy command](https://vercel.com/docs/cli/deploy).

Do not assume a preview URL is private; check its actual access settings.

## 6. Validate the hosted preview

Use the full acceptance list in [release review](release-review.md), including:

1. Open all pages and an invalid route.
2. Test project filters, mobile navigation, keyboard focus, and Contact links.
3. Verify CSS, fonts, JavaScript, favicon, and social image load.
4. Download the résumé and compare it with the approved file.
5. Confirm preview noindex headers and that excluded files are unavailable.
6. Inspect runtime logs and the actual function/static output for unexpected files.

Example response-header check, replacing the example hostname with the returned URL:

```powershell
curl.exe -I https://YOUR-PREVIEW.vercel.app/
```

Expect `X-Robots-Tag: noindex, nofollow` on preview HTML. This controls indexing, not access.

The Flask download route is `/resume/download/`. Vercel can also serve the approved public PDF at `/resume.pdf`; it is intentionally public.

## 7. Configure production metadata

Only after preview review and production approval:

1. Open the project's Domains settings and copy its actual assigned production `.vercel.app` origin.
2. In Settings → Environment Variables, add `SITE_URL` for **Production** only.
3. Set it to the full HTTPS origin, for example `https://YOUR-PROJECT.vercel.app`, without a path, query, fragment, or trailing slash.
4. Keep this environment change out of source control.

Environment changes apply to subsequent deployments, so rebuild/deploy after setting the value. [Environment-variable management](https://vercel.com/docs/environment-variables/managing-environment-variables).

## 8. Publish the reviewed package

Use the **same reviewed staged source**, linked to the same project:

```powershell
npx vercel@latest deploy --prod
```

This is the production publication step. It rebuilds with Production environment settings; it is distinct from reviewing a preview.

Check the assigned production URL, résumé download, canonical and Open Graph URLs, and response headers. With a valid `SITE_URL` and production environment, ordinary pages should no longer return noindex. Filtered/error pages remain noindex.

Record the commit, package manifest, deployment URL, production origin, and release date in the release log.

## 9. Enable Git-based updates

Do this after the CLI preview/release workflow is understood and repository publication is approved.

1. Return to the source checkout and push the reviewed `rebuild/portfolio` branch to remote `portfolio`. This publishes repository source and starts its checks; review the entire commit, not only staged runtime files.
2. Create a separate production branch such as `release/vercel` from an approved revision. Keep `master` reserved for the existing Pages site.
3. In Vercel project settings, connect `Mastr-nil205/portfolio` through GitHub and select `release/vercel` as the production branch. Confirm the chosen source before any import/deploy action; connection/import may start a deployment. If the interface cannot select the intended branch before deploying, stop and keep using the CLI until the branch setup is resolved.
4. Keep the project root at `.` and retain the Flask settings and exclusions.
5. Use development branches/PRs for previews. Merge only reviewed changes into `release/vercel` to trigger production.
6. Confirm GitHub checks pass; use available repository protection settings to require review/checks if desired.

Git-based deployments rebuild from the repository, rather than the local `.release/` folder. Audit the first Git deployment output independently. The included GitHub Actions workflow only validates; Vercel's Git integration performs deployment. [Git deployments](https://vercel.com/docs/git).

## Maintenance and rollback

- Rerun tests after dependency/content changes; review any replacement résumé and update its approved hash.
- Stage a fresh package for each CLI release; link it to the existing project.
- Monitor function usage and errors in Vercel. Recheck plan suitability if the site's purpose changes.
- If production regresses, use the dashboard's rollback controls for a known-good deployment and verify the result. Review any environment changes as well.
- Keep the independent Pages site unchanged until its replacement is explicitly approved.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| 404 on every page | Correct directory, Flask detection, exported `app`, build logs |
| Styles missing | `public/` included; URLs such as `/css/styles.css`; no static-only output override |
| Python import error | Python version, requirements, runtime logs, exclusions |
| Résumé route fails | PDF exists in function package and approval flag is true |
| Production remains noindex | `SITE_URL` set for Production, actual environment correct, redeployed afterward |
| Invalid `SITE_URL` | Use only an HTTPS origin; omit `/portfolio/` |
| A new project appears on every release | Link each fresh package to the existing project |
| Legacy source deploys | Wrong Git branch/root; use the approved Flask branch |

Hosted commands in this guide have not yet been executed for this project. Local tests do not establish Vercel runtime compatibility; the preview checks are required.
