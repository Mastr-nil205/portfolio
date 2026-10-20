# Execution workflow

Follow [AGENTS.md](../AGENTS.md), [architecture](architecture-proposal.md), and [plan](implementation-plan.md).

1. Inspect branch/working tree and current requirements.
2. Select a focused task with satisfied dependencies.
3. Implement within Flask/Jinja and public-content boundaries.
4. Run relevant tests and inspect output.
5. Record results, limitations, and next task.

Flask implementation and design A are approved; do not ask again. Continue independent work when evidence is missing; never invent content.

States: `todo`, `in-progress`, `blocked` with reason, `review`, `done` with evidence. Scaffolding is not content verification.

Review a concrete local preview before external deployment. Preview/production uploads require public-only source and artifact checks. Production or changes to existing Pages need explicit approval.

Pages currently selects `master:/docs`; do not merge documentation there. Vercel connection has not been established.
