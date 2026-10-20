# Flask portfolio implementation plan

Updated 2026-10-20. Supersedes the earlier framework/venture roadmap. Flask/Jinja implementation and design A are approved; deployment is not.

| ID | Task | Acceptance criteria | State |
| --- | --- | --- | --- |
| 01.1 | Repository/live audit | Source, Git, Pages source, rollback recorded | done |
| 01.2 | Development branch | Separate branch; legacy/history retained | done |
| 01.3 | Architecture comparison | Static/Flask tradeoffs, Python role, structure, decision | done |
| 01.4 | Privacy migration | Private backup; obsolete/private content removed from checkout | done |
| 02.1 | Bootstrap directions | Two compositions; selected A recorded | done |
| 02.2 | Flask/data foundation | Exported app, validated JSON layer, pinned dependencies | done |
| 02.3 | Shared design | Jinja, Bootstrap customization, local assets, accessible menu | done |
| 02.4 | Homepage preview | Accurate content; desktop/mobile inspected | done |
| 03.1 | Public pages | Home, About, Experience, Projects, Resume, Contact, 404 | done |
| 03.2 | Project behavior | GET search/categories, detail lookup, empty states, safe errors | done |
| 03.3 | Verified content | Current resume, employment, approved project/contact evidence | done: user-supplied resume reconciled |
| 03.4 | Resume download | Actual approved PDF with correct behavior | done: unchanged approved PDF; download tested |
| 04.1 | Public-only staging | Allowlist, exclusions, source/artifact privacy checks | done |
| 04.2 | Vercel preparation | Discovery, runtime, exclusions; no deployment mutation | done |
| 04.3 | Hosting review | Hobby, usage, environments, maintenance/rollback documented | done |
| 05.1 | Application tests | Routes, query validation, escaping, content, prefix/assets | done |
| 05.2 | HTML/JS checks | Rendered structure, labels, local links, JS syntax | done |
| 05.3 | Browser review | Desktop/mobile, keyboard, narrow width, reduced motion | partial: Chrome checks passed; full accessibility/device audit pending |
| 05.4 | QA report | Actual results, limitations, release blockers | done |
| 06.1 | Preview readiness | Local checks and privacy pass; exact upload scope reviewed | done |
| 06.1a | Continuous checks | GitHub Actions tests, syntax checks, local staging; no deployment | prepared; local commands pass, hosted run pending |
| 06.1b | Release review | PR description, upload scope, preview acceptance, rollback | prepared in release-review.md and pull-request.md |
| 06.2 | Vercel preview | Authorized account/connection and verified preview | pending approval/access |
| 06.3 | Production review | Complete content, Hobby review, revision, rollback, approval | pending |
| 06.4 | Publication | Approved release; legacy site preserved | pending |

Deliverables by phase: architecture decision; local homepage preview; functional career portfolio; public-only deployment package; QA report; approved live website.

## Work log

- Existing site/publication audited in `repository-audit.md`.
- `rebuild/portfolio` fast-forwarded to README-only remote revision `138e8ad21f1ea0ff1a3a62224beae0cffb2775ae`.
- An uncommitted Astro prototype was built before the stack revision, never published.
- User selected design A and explicitly confirmed Flask/Jinja after clarification.
- Original brief/prototype preserved in private storage outside checkout; obsolete preview stopped.
- Flask migration implemented. 26 pytest checks pass; JavaScript syntax passes; Chrome desktop/mobile reviewed. See qa-report.md. No commits, pushes, Pages changes, or deployments.
- User-authorized LinkedIn reviewed, then reconciled to the supplied résumé: four employer entries, updated Ryder title, combined Infios period. PDF download and résumé email integrated; 26 tests pass.
- Prepared GitHub Actions validation and release/PR review documents. Local workflow commands pass. A local development checkpoint is being recorded; remote push and Vercel preview require the next authorized publication step.
