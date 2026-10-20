# Local QA — 2026-10-20

Implementation is ready for local review, not production release.

## Passed

- 26 pytest cases: seven rendered pages, strict HTML parsing, labels, unique IDs, internal links/assets, query filtering/escaping/validation, missing pages, restricted local file access, résumé approval gating, unpublished project exclusion, mount paths, canonical origin, preview noindex, staging allowlist.
- Both JavaScript modules pass Node syntax checks.
- Chrome homepage screenshots inspected at 1440×1000 and 390×844; experience inspected at desktop and narrow mobile sizes.
- Project search inspected at 320px: keyboard submission, visible submit button, matching and empty states. No horizontal overflow in the inspected narrow search and desktop experience views.
- Mobile menu opens, Escape closes it and returns focus to the button. Fixed header wrapping at 320px.
- No warning/error console entries observed in the inspected preview.
- Reduced-motion CSS disables transitions/animations and smooth scrolling; navigation remains visible without JavaScript by source inspection.
- New source and staged text scan found no excluded venture names. Social image inspected and limited to personal technical identity.
- Allowlisted local staging: 43 files, 443,285 bytes. SHA-256 manifest stored beside the package under ignored `.release/`.
- Git branch is `rebuild/portfolio`; legacy `index.htm` and `stylesheets/main_index.css` have no diff. Git diff whitespace check passed.

Follow-up accessibility review fixed input-border contrast and explicit button focus styling, enlarged smaller standalone targets, verified skip-link focus and keyboard filter submission, and checked all seven public pages at 320px for horizontal overflow. See [accessibility review](accessibility-review.md) for ratios, criteria, and remaining manual checks. A fresh staging package supersedes the earlier package after these CSS changes; use the newest timestamped package and its manifest.

## Content

The supplied public résumé is now the primary source for four employer entries. Infios is grouped into February 2024–February 2026, and Ryder uses the résumé title Systems Configuration Engineer. The website summaries omit numerical claims; the original PDF remains unchanged. This is user-supplied evidence, not independent employer verification.

The two-page résumé was visually reviewed, copied unchanged, and checked by SHA-256. Download status, MIME type, attachment filename, exact bytes, and Contact mailto are tested. Contact now includes the email supplied in the public résumé, alongside LinkedIn and GitHub. One actual in-progress portfolio project is documented, including AI assistance.

## Limits and release gates

- No Vercel build, runtime, CDN routing, Git integration, preview, or production deployment was executed. Configuration still needs platform validation after upload authorization.
- Browser checks are targeted Chrome checks, not a full screen-reader/WCAG audit or Safari/Firefox/physical-device test. Reduced-motion was inspected in CSS, not emulated in browser. No Lighthouse score is claimed.
- The exact final production artifact, PDF, metadata origin, and complete public content must be reviewed before release.
- Current Hobby restrictions are documented in deployment.md; eligibility is not guaranteed. Uncertain use cases require clarification with Vercel Support.
- Existing Pages configuration remains unchanged, including the previously identified missing `/docs` source issue.

No pushes, merges, hosting connections, or deployments were performed. A local Git checkpoint is being prepared for release review.

GitHub Actions validation was added after the implementation checks. Its test, JavaScript syntax, and packaging commands pass locally; the hosted Linux workflow has not run yet. See release-review.md for upload scope and preview acceptance.
