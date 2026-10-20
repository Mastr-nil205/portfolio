# Repository and deployment audit

Task: 01.3
Audited: 2026-10-20 (America/Indianapolis)
Status: Complete. Read-only inspection; no publication changes.

## Findings

The existing website is online, but the current Pages configuration cannot rebuild the remote revision successfully. Pages now selects `master:/docs`; that directory does not exist on the remote. The last successful build used the repository root. Our new local `docs/` contains planning material and must not be merged into the publication branch under this configuration.

## Repository state

| Item | Verified value |
| --- | --- |
| Repository | Public, `Mastr-nil205/portfolio` |
| Remote name | `portfolio` |
| Remote default branch | `master`, confirmed by public API and `git ls-remote --symref` |
| Remote HEAD | `138e8ad21f1ea0ff1a3a62224beae0cffb2775ae` |
| Local development branch | `rebuild/portfolio` |
| Local HEAD | `9c693e25ef2917490c26365af75ba48ea2a8b48c` |
| Remote delta | One commit, `Create README.md`; adds three lines to README only |
| Remote files | `README.md`, `index.htm`, `stylesheets/main_index.css` |
| Remote deployment code | No checked-in `.github/workflows/`, package manifest, or build configuration |
| Local working tree at audit start | `AGENTS.md` and `docs/` untracked; no tracked application changes |

Evidence: [repository metadata](https://api.github.com/repos/Mastr-nil205/portfolio), [remote tree](https://api.github.com/repos/Mastr-nil205/portfolio/git/trees/138e8ad21f1ea0ff1a3a62224beae0cffb2775ae?recursive=1), [README commit](https://github.com/Mastr-nil205/portfolio/commit/138e8ad21f1ea0ff1a3a62224beae0cffb2775ae).

Recommendation: incorporate the README-only commit into the development branch before foundation work, after rechecking working-tree and remote state. A fast-forward is appropriate if ancestry and the current delta remain unchanged. This audit did not fetch, merge, commit, or push.

## Actual GitHub Pages configuration

Read directly from the authenticated browser's [Pages settings](https://github.com/Mastr-nil205/portfolio/settings/pages):

| Setting | Observed value |
| --- | --- |
| Source mode | Deploy from a branch |
| Branch | `master` |
| Folder | `/docs` |
| Public URL | `https://mastr-nil205.github.io/portfolio/` |
| Custom domain | Empty |
| Enforce HTTPS | Enabled and required for the default domain |
| Environment | `github-pages` |
| Workflow | GitHub-managed `pages-build-deployment`, path `dynamic/pages/pages-build-deployment` |
| Last deployed link | Successful run `39174299883` |

The presence of a managed Actions workflow does not mean the Pages source setting is “GitHub Actions.” The selected mode is explicitly branch publication.

## Deployment history and failure diagnosis

Both recent runs used remote commit `138e8ad21f1ea0ff1a3a62224beae0cffb2775ae`.

| Run | Local time on October 18, 2026 | Result | Build source |
| --- | --- | --- | --- |
| [39174299883](https://github.com/Mastr-nil205/portfolio/actions/runs/39174299883) | 6:55:13–6:55:50 p.m. EDT | Build and deploy succeeded | `/github/workspace/.` |
| [39174343629](https://github.com/Mastr-nil205/portfolio/actions/runs/39174343629) | 6:55:51–6:56:20 p.m. EDT | Jekyll build failed; upload and deployment skipped | `/github/workspace/./docs` |

The [failed build log](https://github.com/Mastr-nil205/portfolio/actions/runs/39174343629/job/117813807872) identifies a missing `/github/workspace/docs` directory. The [successful build log](https://github.com/Mastr-nil205/portfolio/actions/runs/39174299883/job/117813680158) identifies the repository root as its source and `_site` as its destination.

This confirms a source-directory mismatch. It is not evidence of a failure in the proposed Astro application, which has not been created. The failed run did not deploy; settings still identify the preceding successful run as the live deployment.

## Live website inspection

Checked using HTTP GET responses plus the existing Chrome tab's DOM and desktop screenshot. No form was submitted, job rerun, or setting saved.

| URL relative to `/portfolio/` | HTTP result | Observation |
| --- | --- | --- |
| `/` | 200 | Existing portfolio, title “Luigi Josue: Web Development Portfolio” |
| `/index.htm` | 200 | Existing HTML entry point |
| `/stylesheets/main_index.css` | 200 | Stylesheet available |
| `/index.js` | 404 | Referenced script is missing in production as well as locally |
| `/404.html` | 404 | Generic GitHub Pages error page; no custom recovery page |

The visible site retains the old entry-level developer/cloud-services positioning, a large pale-teal introduction, text-only skills, and a contact form. Header/footer destinations and social links mostly point to `#`. No real project case studies, employment timeline, venture pages, or resume link are exposed in the inspected page.

The form has no working submission mechanism in the inspected code, and its visible controls lack correctly associated labels. Its mailbox destination was not tested. The legacy email address remains unverified as a current preferred contact.

This was an initial desktop/content audit, not the phase 05 accessibility or responsive test suite. No mobile screenshot review, comprehensive contrast measurement, performance benchmark, or exhaustive external-link test was performed.

## Rebuild and publication implications

1. Keep development on `rebuild/portfolio`. Do not push planning documents to `master` or merge the development branch while `master:/docs` is the active publication source.
2. Reserve `docs/` for planning and review records; never use it as Astro's output directory. Publishing that folder could replace the website with planning material.
3. At approved release time, transition Pages to the reviewed GitHub Actions workflow and publish only Astro's generated `dist/` artifact. Do not upload the repository root, `docs/`, or private evidence.
4. Preserve the `/portfolio/` base. Include a compatibility decision for existing `/index.htm` links in the migration proposal.
5. Keep PR build verification separate from deployment. Any publishing action remains subject to G4, including changing the Pages source setting.
6. The repository itself is public. Excluding documents from the site artifact does not make committed source documents private; review the master brief and other planning material for public-repository suitability before pushing.

## Rollback baseline

Known working source revision: `138e8ad21f1ea0ff1a3a62224beae0cffb2775ae`. Known working build source: repository root. Successful run: `39174299883`; deployment ID: `7161989674`.

Do not use the current `/docs` setting as a known-good rollback configuration. Before release, prepare and validate a recovery artifact from the known working revision or an equivalent isolated legacy build, and record how the approved release workflow can publish it. If reverting to branch publication is chosen instead, the source must be the legacy root and must not expose newly added planning files. Choose and test the concrete rollback mechanism in phase 06; no rollback was performed here.

## Access and remaining work

- Sandbox network access was blocked; approved read-only external requests succeeded.
- Saved GitHub CLI credentials returned HTTP 401. Public API requests and the already authenticated browser provided the required evidence without changing credentials.
- Anonymous Pages API calls returned 404; the authenticated settings UI resolved this access gap.
- Repair CLI authentication before tasks that require authenticated CLI writes, or use an appropriate authenticated supported interface. This did not prevent completion of the audit.
- Next task: **01.5**, finalize the architecture/migration proposal using these verified facts, then present G1 for review.
