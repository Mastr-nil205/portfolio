# Portfolio instructions

## Current decisions

The user explicitly selected Flask/Jinja implementation on 2026-10-20 after resolving conflicting static-first instructions. This supersedes the earlier Astro proposal. Design direction A, technical editorial, is approved. Implementation is authorized; production deployment and changes to the existing GitHub Pages site are not.

Read `docs/portfolio-brief.md`, `docs/architecture-proposal.md`, `docs/implementation-plan.md`, `docs/content-inventory.md`, and `docs/deployment.md` before work.

## Stack and structure

- Python 3.13, Flask, Jinja2, semantic HTML5, Bootstrap 5, custom CSS, vanilla JavaScript, pytest.
- No Astro, React, Next.js, Tailwind, TypeScript, Django, database, accounts, or administrative UI.
- `app.py` exports `app`; `portfolio_data.py` owns validated JSON reads and project queries; templates own presentation.
- Use shared Jinja templates and Bootstrap containers, rows, columns, and component variables. Customize appearance with CSS tokens; do not use a stock theme.
- Public assets live in `public/`, served by Vercel's CDN in production. Local-only asset routes must serve only that directory.
- No persistent filesystem writes in request handlers or debug mode in production. Escape untrusted content; never pass request data into template source or mark it safe.
- Bound query lengths, validate category choices, reject unexpected parameters, and return a real 404 for unknown project slugs.
- Keep repository methods separate from templates so storage can change later without redesigning pages.

## Content and privacy

- Public routes: Home, About, Experience, Projects, Resume, Contact. No business pages, promotions, pricing, quote forms, or sales calls to action.
- Keep private drafts outside this repository and deployment artifacts. Hidden HTML, unlinked pages, robots rules, and CSS hiding are not privacy controls.
- Never restore archived private material to the repository. Earlier drafts were preserved in private local storage outside this checkout.
- Inspect public source, metadata, images, downloads, data, and deployment bundles for private content before any push or deployment.
- Use the user-supplied public résumé (received 2026-10-20) as the primary employment source; LinkedIn is supporting context. Never invent roles, dates, achievements, skills, projects, metrics, or credentials.
- The approved résumé is in public/resume.pdf; its SHA-256 is recorded in data/profile.json. Its email is approved through the public résumé submission. Preserve download integrity; review replacements before publication.
- The user confirmed `https://www.linkedin.com/in/luigi-josue` for publication. GitHub identity is supported by the existing repository.
- Distinguish professional experience from independent work and learning.

## Git and deployment

- Work on `rebuild/portfolio`; remote is `portfolio`, default/publication branch `master`. Inspect state and preserve unrelated changes.
- Git ownership requires approved execution as the Windows owner here. Do not bypass checks or modify refs manually.
- Keep `index.htm` and `stylesheets/main_index.css` unchanged until replacement approval. Exclude them from the new Vercel deployment.
- Existing Pages selects `master:/docs`; do not merge planning documents into that active source. See `docs/repository-audit.md`.
- Vercel is the intended new host, using a default `.vercel.app` domain. No hosting account, repository connection, or deployment has been created.
- Prepare local tests and a public-only deployment package before external publication. Preview deployment also transmits files; inspect it first and observe the current approval scope.
- Never guarantee Hobby eligibility. Check official terms and flag uncertain use cases for Vercel Support. Do not contact others without authorization.
- Do not deploy production, change Pages settings, or merge into the publication branch without explicit approval.

## Execution and verification

- Work through focused tasks; update the plan with results, evidence, and blockers. Continue authorized reversible work without repeated confirmation. Do not delegate unless requested.
- Run pytest for routes, filtering, escaping, missing content, URL prefixes, assets, and privacy boundaries. Validate rendered HTML and JavaScript syntax.
- Inspect desktop/mobile layouts and keyboard navigation; honor reduced motion.
- Test root deployment and `/portfolio/` mounting. Flask cannot execute on GitHub Pages; preserving the old site is separate from hosting the new application.
- Report unrun platform/browser checks honestly. Page scaffolding does not complete content verification.
