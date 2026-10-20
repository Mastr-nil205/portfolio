# Release review

Prepared 2026-10-20. Local implementation is complete; external deployment requires the user's approval.

## Proposed next action

Create a Vercel **preview** from the newest reviewed `.release/` package. This uploads the personal portfolio, public résumé (including its email and phone), approved experience, and public assets to Vercel. No custom domain, paid resource, database, or production promotion is proposed.

Use the existing account if available. Account login must be completed through the normal sign-in flow; do not share credentials in chat. Any project import that would trigger a production deployment must be avoided until production is explicitly approved.

The allowlisted package contains:

- `app.py`, `portfolio_data.py`, Python requirements/version and runtime configuration.
- Shared Jinja templates, approved JSON content, public CSS/JavaScript/fonts/images/vendor assets.
- The unchanged approved résumé PDF.

The adjacent hash manifest is for local review, not an application asset. Private archives, development docs, caches, tests, legacy Pages files, and the virtual environment are excluded.

## Preview acceptance

1. Confirm Vercel detects Flask and Python 3.13, and inspect build/function output.
2. Verify every public route, unknown-page 404, search/category behavior, and invalid-query errors.
3. Confirm CDN assets load, JavaScript works, fonts render, and no console/CSP failures appear.
4. Download the résumé; compare SHA-256 with `data/profile.json`. Confirm attachment filename and PDF MIME type.
5. Check preview noindex headers, narrow layouts, keyboard navigation, and Contact links.
6. Confirm excluded files cannot be retrieved and no commercial drafts entered static assets or the function bundle.
7. Review current Hobby restrictions against the final content and intended use; escalate uncertain eligibility to Vercel Support through the user.

## Production remains a separate decision

After preview review, record the approved revision and assigned origin. Set `SITE_URL` for production, verify canonical/social metadata, and explicitly approve production promotion.

Preserve the old Pages site and its settings. Do not merge this branch into `master` under the current `master:/docs` Pages configuration.

## Git-based deployment

The prepared GitHub Actions workflow validates pull requests and the development branch; it never deploys. Before enabling Vercel Git integration, select an appropriate production branch and confirm import behavior. Do not let a branch push become an unreviewed production deployment.

Draft PR text is in `docs/pull-request.md`. No PR, push, Git integration, or hosted workflow run has been performed.

Action syntax was checked against the maintainers' documentation: [checkout](https://github.com/actions/checkout), [setup-python](https://github.com/actions/setup-python), [setup-node](https://github.com/actions/setup-node).
