# Contributing to A11yDaily

Thank you for contributing to A11yDaily.

A11yDaily is a digital accessibility intelligence platform built to collect, organize, explain, and deliver trusted accessibility knowledge.

This guide defines the contribution workflow, quality expectations, and review standards for the project.

## Before You Begin

New contributors should first read:

1. `README.md`
2. `docs/ONBOARDING.md`
3. `docs/VISION.md`
4. `docs/CONSTITUTION.md`
5. `docs/ARCHITECTURE.md`
6. `docs/DOMAIN_MODEL.md`
7. `docs/ENGINEERING.md`
8. Relevant Architecture Decision Records in `docs/adr/`

Contributors working on ingestion should understand this flow:

```text
SourceAdapter
→ RawDocument
→ DocumentNormalizer
→ NormalizedDocument
→ IngestionPipeline
→ PipelineStage
→ KnowledgeAssetFactory
→ KnowledgeAsset
```

## Core Contribution Principles

### Accessibility Is a Release Requirement

New features and changes must preserve or improve accessibility.

The platform should meet WCAG 2.2 Level AA as a minimum baseline.

Accessibility concerns should be addressed during design and implementation, not postponed until after release.

### Preserve Source Trust

A11yDaily must retain clear provenance for collected information.

Contributions must not:

- Remove or obscure original source URLs.
- Replace source content with AI-generated content.
- Present inferred information as verified fact.
- Alter source attribution without justification.
- Introduce ranking systems that hide sponsorship or commercial influence.

### Keep the Domain Independent

Code in `apps/api/app/domain/` must remain independent of infrastructure frameworks.

Domain code must not import:

- FastAPI
- SQLAlchemy
- Alembic
- HTTPX
- feedparser
- Redis clients
- AI provider SDKs

Infrastructure and persistence layers may depend on the domain. The domain must not depend on them.

### Prefer Focused Changes

Each branch and pull request should solve one clearly defined problem.

Avoid combining:

- New features
- Broad refactoring
- Dependency upgrades
- Formatting changes
- Documentation rewrites

into a single pull request unless they are inseparable.

## Development Setup

Follow the complete setup instructions in:

```text
docs/ONBOARDING.md
```

At minimum, verify that these commands work:

```bash
docker compose up --build
make api-lint
make api-test
make web-lint
```

## Branching Strategy

Do not commit directly to `main`.

Create a branch from the latest appropriate base branch.

```bash
git checkout main
git pull
git checkout -b <type>/<short-description>
```

Supported branch prefixes include:

```text
feat/
fix/
docs/
test/
refactor/
chore/
security/
```

Examples:

```text
feat/webaim-rss-source
fix/rss-published-date-parsing
docs/update-ingestion-architecture
test/content-hash-collision
refactor/knowledge-asset-mapper
chore/update-python-tooling
```

Use lowercase, hyphen-separated branch names.

## Commit Messages

Use concise, imperative commit messages.

Preferred format:

```text
<type>: <description>
```

Examples:

```text
feat: add generic RSS source adapter
fix: preserve canonical URL during normalization
docs: add contributor workflow
test: cover missing RSS publication date
refactor: extract knowledge asset mapper
chore: update Python dependencies
```

A commit should represent one logical change.

Avoid vague messages such as:

```text
updates
changes
fix stuff
more work
wip
```

Temporary work-in-progress commits may be used locally but should be cleaned up before merge when practical.

## Coding Standards

### Python

Python code should:

- Include type hints.
- Use clear, descriptive names.
- Prefer small functions and classes.
- Avoid hidden side effects.
- Use modern SQLAlchemy patterns.
- Follow Ruff and Black formatting rules.
- Include docstrings where they clarify responsibility.
- Avoid unnecessary inheritance or abstraction.

Run:

```bash
make api-lint
make api-test
```

### TypeScript and React

Frontend code should:

- Use semantic HTML.
- Preserve keyboard accessibility.
- Provide accessible names and labels.
- Avoid unnecessary ARIA.
- Use strict TypeScript types.
- Follow the existing component and routing conventions.
- Pass ESLint and accessibility linting rules.

Run:

```bash
make web-lint
```

### Naming

Prefer explicit names over abbreviations.

Use:

```text
KnowledgeAssetRepository
NormalizedDocument
source_identifier
published_at
```

Avoid names such as:

```text
KAR
NormDoc
src_id
pub_dt
```

Good naming reduces the need for explanatory comments.

## Testing Expectations

Every new behavior should include an appropriate test.

Tests should be:

- Focused.
- Deterministic.
- Independent of execution order.
- Clear about the behavior being verified.
- Free from unnecessary live network access.

### Unit Tests

Use unit tests for:

- Domain behavior.
- Normalization.
- Pipeline stages.
- Factories and mappers.
- Error handling.
- Adapter parsing with mocked responses.

### Integration Tests

Use integration tests for:

- PostgreSQL repositories.
- Alembic migrations.
- API endpoints.
- Cross-layer persistence behavior.

### Live Smoke Tests

Live external sources should not normally be part of the default test suite.

Live checks may fail because of:

- Network availability.
- Rate limits.
- Source downtime.
- Feed changes.
- Redirects.
- TLS or DNS issues.

Keep live smoke tests under `apps/api/scripts/` or a separately marked integration suite.

### Regression Tests

Every bug fix should include a test that fails before the fix and passes afterward.

## Database Changes

All database schema changes require an Alembic migration.

Generate migrations inside Docker:

```bash
docker compose run --rm api \
  alembic revision --autogenerate -m "describe the migration"
```

Review the generated migration before applying it.

Apply migrations:

```bash
docker compose run --rm api alembic upgrade head
```

Verify:

```bash
docker compose run --rm api alembic current
```

A migration should include both `upgrade()` and `downgrade()` behavior whenever practical.

Do not edit an already-shared migration to change production history. Create a new migration instead.

## Dependency Changes

Dependency additions and upgrades should be intentional.

Before adding a dependency, consider:

- What problem does it solve?
- Can the standard library solve the problem adequately?
- Is the package actively maintained?
- What is its security history?
- Does it add significant transitive dependencies?
- Is its license compatible with the project?
- Does it support our Python or Node versions?

When changing dependencies:

- Update the appropriate dependency file.
- Rebuild the relevant Docker image.
- Run the complete test suite.
- Document any compatibility concerns.
- Avoid unrelated dependency upgrades in feature pull requests.

## Documentation Requirements

Documentation is part of the deliverable.

Update documentation when a contribution changes:

- Architecture.
- Domain language.
- Setup instructions.
- Public behavior.
- Database structure.
- Ingestion flow.
- Developer commands.
- Supported sources.
- Accessibility requirements.

Major architectural decisions require an Architecture Decision Record.

## Architecture Decision Records

Create an ADR when a change introduces or alters a significant architectural decision.

ADR location:

```text
docs/adr/
```

Suggested filename:

```text
0002-staged-ingestion-pipeline.md
```

An ADR should include:

- Status
- Context
- Decision
- Alternatives considered
- Consequences
- Related documents or issues

Do not create an ADR for routine implementation details.

## Pull Request Requirements

Every pull request should include:

- A clear title.
- A concise summary.
- The reason for the change.
- The implementation approach.
- Testing performed.
- Documentation changes.
- Known limitations or follow-up work.
- Screenshots or recordings for meaningful interface changes.

A good pull request title follows the commit style:

```text
feat: add WebAIM RSS source
fix: handle RSS entries without GUIDs
docs: add contributor workflow
```

## Pull Request Size

Prefer small, reviewable pull requests.

A practical target is approximately 200–400 changed lines when possible, excluding generated migrations and lockfiles.

Larger changes should be split into logical stages unless splitting would make the work harder to understand or test.

## Review Expectations

Reviewers should evaluate:

- Correctness.
- Accessibility.
- Security.
- Test coverage.
- Naming.
- Dependency direction.
- Error handling.
- Maintainability.
- Documentation.
- Scope discipline.

Review comments should explain the underlying concern, not merely request a preferred style.

Contributors should respond to each substantive review comment by:

- Applying the change.
- Explaining why no change is needed.
- Asking for clarification.

Resolve conversations only after the concern is addressed.

## Definition of Done

A contribution is complete when:

- The requested behavior is implemented.
- Tests cover new or changed behavior.
- Existing tests pass.
- Linting passes.
- Type hints are present.
- Error handling is appropriate.
- Accessibility has been reviewed.
- Documentation is updated when needed.
- Database migrations are included when needed.
- No secrets or generated caches are committed.
- The pull request is focused and reviewable.
- All substantive review comments are resolved.

## Accessibility Review Checklist

For user-facing changes, verify:

- Keyboard operation.
- Visible focus.
- Logical heading structure.
- Semantic landmarks.
- Accessible names.
- Form labels and instructions.
- Error identification.
- Color contrast.
- Information not conveyed by color alone.
- Screen-reader output.
- Responsive zoom and reflow.
- Reduced-motion preferences where applicable.

Automated checks do not replace manual accessibility testing.

## Security and Privacy

Never commit:

- API keys.
- Passwords.
- Tokens.
- Private credentials.
- `.env` files.
- Personal user information.
- Production database exports.

Treat all external content as untrusted input.

Adapters, normalizers, and API endpoints should account for:

- Malformed data.
- Unexpected encodings.
- Excessively large payloads.
- Unsafe HTML.
- Invalid URLs.
- Network timeouts.
- Redirect behavior.
- Duplicate content.

Security concerns should be reported privately to the project owner rather than disclosed publicly before a fix is available.

## Repository Hygiene

Before committing:

```bash
git status
```

Check for accidental additions such as:

```text
.DS_Store
.env
.venv/
node_modules/
.next/
__pycache__/
.pytest_cache/
.ruff_cache/
*.pyc
local logs
temporary exports
```

Only stage files related to the intended change.

## Suggested First Contributions

Good onboarding issues include:

- Add an accessibility RSS source using `RSSSourceAdapter`.
- Add a parser regression test.
- Improve setup documentation.
- Add structured logging to an ingestion component.
- Add error handling for a specific malformed feed.
- Improve a domain or pipeline unit test.
- Document an architecture decision already reflected in the code.

Avoid assigning major domain redesign, authentication, billing, AI architecture, or persistence restructuring as a first contribution.

## Getting Help

When asking for help, include:

- The command you ran.
- Your current directory.
- Your current branch.
- The complete error output.
- What you expected.
- What you already tried.

Useful diagnostic commands include:

```bash
pwd
git status
docker info
docker compose ps
python --version
which python
make api-test
make api-lint
```

## Code of Conduct

Contributors are expected to communicate respectfully and constructively.

A11yDaily serves a community centered on inclusion. Project collaboration should reflect that mission.

Harassment, discrimination, personal attacks, and dismissive treatment of accessibility concerns are not acceptable.

## License

By contributing, you agree that your contributions may be distributed under the repository’s license.

The project license should be reviewed before accepting outside contributions.
