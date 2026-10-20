# Architecture and migration decision

2026-10-20: **Flask/Jinja approved for implementation by the user.** Production remains unapproved.

## Audit and reuse

The tracked legacy site is one Bootstrap HTML page and stylesheet. The uncommitted prototype introduced Astro before the revised requirements. It was archived outside the repository; framework source, build output, Node dependencies, and configuration were retired.

Reuse selected dark editorial design, suitable CSS, licensed fonts, factual biography, and Git history. Replace framework-specific routes/components and excluded business content. Keep legacy `index.htm` and stylesheet unchanged. See [repository audit](repository-audit.md).

## Comparison

| Consideration | Static HTML with optional Python/Jinja generation | Flask/Jinja on Vercel |
| --- | --- | --- |
| Runtime | CDN files; simplest operation | Python function renders HTML |
| Template reuse | Build time | Request time |
| Search/filter | Vanilla JS over public data or generated categories | Validated GET query parameters |
| GitHub Pages | Generated files supported | Flask cannot execute there |
| Maintenance | Generator/content | Dependencies, routes, request validation, runtime |
| Learning fit | Python automation and frontend | Direct Flask, Jinja, data-layer and test practice |
| Database | Not needed | Not needed |

Static generation is simplest for brochure content. Flask is justified by the user's explicit learning/maintenance preference and requested server-rendered project lookup/filtering. The user selected it after clarification. No requested feature requires PostgreSQL or Django.

## Structure

```text
app.py                   # factory, exported app, routes, errors
portfolio_data.py        # public JSON validation and queries
requirements.txt         # pinned production dependencies
requirements-dev.txt     # tests and validation
pyproject.toml           # Python/tool configuration
templates/
  base.html
  components/
  home.html
  about.html
  experience.html
  projects.html
  project_detail.html
  resume.html
  contact.html
  error.html
data/
  profile.json
  projects.json
  experience.json
  skills.json
public/
  css/
  js/
  vendor/
  fonts/
  images/
  resume.pdf             # only after approved resume is supplied
tests/
scripts/                 # validation/public-only staging
docs/                    # public-safe development records
```

## Behavior

- Export `app` in `app.py`; application factory supports tests.
- Routes: `/`, `/about/`, `/experience/`, `/projects/`, `/projects/<slug>/`, `/resume/`, `/contact/`, real 404.
- Search/category filtering uses GET; restrict parameter names, category values, and query length. Jinja autoescaping handles displayed query values.
- Unknown slugs return 404. Missing resume produces no false download.
- Data querying lives outside templates; a future database repository can preserve template contracts.
- Use `url_for` and mount-aware assets. Test root and `/portfolio/` mounts; this is not Pages runtime compatibility.
- Vercel serves `public/` from its CDN. Local asset routes are restricted to that directory.
- No request-time writes, sessions, secrets, background jobs, or database.

## Python and migration

Python provides routes, JSON validation/filtering, tests, and an allowlisted deployment staging tool. No frontend package manager is needed.

Migration: preserve old drafts privately → retire prototype → sanitize public files → implement Flask/Jinja and Bootstrap → integrate verified content → test behavior/privacy/layout → prepare preview and release review.

Private archives never enter the repository or bundles. Source cleanup, explicit staging, exclusions, and tests overlap; `.gitignore` alone does not protect tracked material.

## Platform implications

Vercel discovers Flask's exported `app`, runs it as a function, and serves `public/` separately. Its development server is not a production server. [Flask deployment](https://vercel.com/docs/frameworks/backend/flask).

Python 3.13 is supported and matches local tooling. Python bundles include reachable project files unless excluded. Keep runtime dependencies small and account for function limits. [Python runtime](https://vercel.com/docs/functions/runtimes/python).

See [deployment notes](deployment.md) for environments, costs, Hobby review, and rollback.
