# Vercel deployment and maintenance

Official documentation reviewed 2026-10-20. Target: Flask/Jinja on a default `.vercel.app` domain. No Vercel project, account connection, preview, or production deployment created.

For executable step-by-step procedures, use [local deployment](local-deployment.md) and [Vercel deployment](vercel-deployment.md). This document records architecture, policy, and maintenance context.

## Runtime and environments

Export `app` in `app.py`. Pin Python 3.13 and runtime dependencies. Vercel detects Flask, runs it as a function, and serves `public/` from its CDN. Local assets use matching URLs. [Flask guide](https://vercel.com/docs/frameworks/backend/flask).

No persistent filesystem writes, background loops, or reliance on process memory surviving requests. Current features need no database or credentials. The documented standard Python bundle limit is 500 MB; execution and usage limits also apply. [Python runtime](https://vercel.com/docs/functions/runtimes/python), [limits](https://vercel.com/docs/limits).

| Variable | Purpose |
| --- | --- |
| `SITE_URL` | Approved production origin for canonical/social URLs, once assigned |
| `VERCEL_ENV` | Platform environment; non-production responses are noindex |
| `VERCEL` | Platform flag; disables Flask's local asset routes when present |

No session secret is needed without sessions/forms. Never commit confidential `.env` values.

## Public-only delivery

Stage only modules, templates, approved JSON, public assets, and runtime configuration. Exclude docs, tests, caches, virtual environments, legacy files, and obsolete builds from the function bundle. Private drafts must be outside the repository, not merely unlinked.

Run `python scripts/stage_release.py` for a fresh allowlisted `.release/` directory and adjacent SHA-256 manifest. This stages locally and never deploys. It rejects unpublished project records and an unapproved résumé PDF. Review the entire staged directory before an authorized upload. `LOCAL_ASSETS` is an application/test configuration value, not an environment variable.

Audit source and staged output before upload; inspect actual Vercel output before claiming platform validation. Do not enable auto-deployment before the connected branch is public-safe.

## Preview and production

Git integration supports branch/PR previews. Select the production branch deliberately: importing can deploy immediately, so connection is an external deployment step, not harmless setup. [Git deployments](https://vercel.com/docs/git), [environments](https://vercel.com/docs/deployments/environments).

When authorized, import the repository or upload audited staging, confirm Flask settings, review a preview, then approve the production revision. Preview URLs are not assumed private.

Keep existing Pages unchanged. Flask cannot execute there. A future static export would be a separate explicit requirement.

## Hobby and costs

Hobby is restricted to personal, non-commercial use. Removing business advertising, paid-service offers, and sales calls to action reduces obvious conflicts but does not guarantee eligibility. Review complete content and use context; uncertain cases should be confirmed with Vercel Support by the user. [Hobby](https://vercel.com/docs/plans/hobby), [terms](https://vercel.com/legal/terms).

Hobby has no subscription charge within allowances, but usage is limited and capabilities may pause when limits are exceeded. Flask adds function usage compared with static hosting. If commercial use returns, reassess eligibility and paid pricing. No paid resources are authorized. [Pricing](https://vercel.com/pricing).

## Maintenance and rollback

Update dependencies and vendored Bootstrap deliberately, preserving licenses and rerunning tests/browser checks. Edit approved JSON; verify evidence before changing employment or outcomes. Recheck Hobby policy/usage when releasing or changing purpose.

Record deployed commit and URL; rollback to a verified Vercel deployment if needed. Pages remains an independent legacy fallback; do not redirect or unpublish it automatically.

Release prerequisites: verified resume/history, complete QA, public-content review, authorized account connection, actual preview validation, production approval.
