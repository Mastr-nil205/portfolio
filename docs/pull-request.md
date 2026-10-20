# Rebuild personal portfolio with Flask and Bootstrap

The legacy single-page portfolio is replaced for the proposed Vercel deployment by a maintainable Flask/Jinja application with Home, About, Experience, Projects, Resume, Contact, and project-detail pages. The approved navy/teal design extends Bootstrap and uses local fonts plus small vanilla JavaScript modules.

Professional history and the downloadable PDF follow the user-supplied résumé. Projects describe actual work in progress; the public site excludes business promotions. JSON content is separate from templates. Server-rendered project filters validate input, and missing pages return real error responses.

The legacy Pages files remain unchanged. Deployment packaging excludes them, development documentation, caches, and tests. A local allowlist creates release files with a SHA-256 manifest; no hosting connection or deployment is included in this change.

## Validation

- 26 pytest checks pass locally: routes, HTML, links, filtering, escaping, mount prefixes, public-file boundaries, résumé integrity, and release staging.
- JavaScript syntax checks pass.
- Chrome desktop/mobile review and 320px reflow checks completed; focus visibility and form-border contrast improved.
- GitHub Actions workflow added for tests, syntax checks, and local packaging. Its hosted run is pending a push.

## Before release

Review the prepared preview procedure in `docs/release-review.md`. Vercel runtime/CDN behavior and a real preview remain untested. Full screen-reader, browser-engine, and physical-device checks remain outstanding.

Do not merge into `master` while Pages still selects `master:/docs`: that could expose development documentation as the Pages source. Keep publication approval separate from this review.
