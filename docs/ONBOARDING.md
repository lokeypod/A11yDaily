# A11yDaily Developer Onboarding

**Version:** 1.0
**Status:** Active
**Last Updated:** July 2026

## Purpose

This guide helps a new developer understand, run, and contribute to A11yDaily.

A developer completing this guide should be able to:

- Run the full application locally.
- Run linting and automated tests.
- Understand the repository structure.
- Explain the ingestion pipeline.
- Create a branch and submit a focused pull request.

## What A11yDaily Is

A11yDaily is a digital accessibility intelligence platform.

It collects public accessibility information from trusted sources, converts source-specific content into a consistent internal representation, enriches and organizes that information, and delivers it through searchable and personalized experiences.

The platform treats document accessibility—including PDF/UA, Microsoft Word, PowerPoint, Excel, EPUB, OCR, and document-remediation workflows—as a first-class domain alongside web, mobile, legal, standards, tools, research, and community content.

## Recommended Reading

Read these documents before changing production code:

1. `README.md`
2. `docs/VISION.md`
3. `docs/CONSTITUTION.md`
4. `docs/PRD.md`
5. `docs/ARCHITECTURE.md`
6. `docs/DOMAIN_MODEL.md`
7. `docs/ENGINEERING.md`
8. Relevant files in `docs/adr/`

The Vision explains what A11yDaily should become.

The Constitution defines the principles used to make product and engineering decisions.

The architecture and domain documents explain how the system is structured.

## Prerequisites

Install:

- Git
- Docker Desktop
- Visual Studio Code
- Python 3.13 or a compatible supported version
- Node.js
- npm

Recommended Visual Studio Code extensions are listed in:

```text
.vscode/extensions.json
```

## Clone the Repository

```bash
git clone <repository-url>
cd A11yDaily
```

Replace `<repository-url>` with the GitHub repository URL.

## Create the Local Python Environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r apps/api/requirements.txt
```

Verify:

```bash
python --version
which python
```

The interpreter path should point to:

```text
A11yDaily/.venv/bin/python
```

In Visual Studio Code, select the same interpreter:

```text
Command Palette
→ Python: Select Interpreter
→ .venv/bin/python
```

## Environment Configuration

Create the local environment file:

```bash
cp .env.example .env
```

Do not commit `.env`.

Secrets and machine-specific settings must remain outside Git.

## Start the Application

Ensure Docker Desktop is running.

From the repository root:

```bash
docker compose up --build
```

Verify:

```text
Web: http://localhost:3000
API health: http://localhost:8000/health
```

The Docker environment includes:

- Next.js
- FastAPI
- PostgreSQL with pgvector
- Redis

## Common Commands

Run API linting:

```bash
make api-lint
```

Run API tests:

```bash
make api-test
```

Run frontend linting:

```bash
make web-lint
```

Start the development stack:

```bash
make dev
```

Stop the development stack:

```bash
make down
```

Check repository state:

```bash
git status
```

## Repository Tour

```text
A11yDaily/
├── .github/
├── .vscode/
├── apps/
│   ├── api/
│   └── web/
├── docs/
├── docker-compose.yml
├── Makefile
└── README.md
```

### `.github/`

Contains GitHub-specific configuration, including workflows and future issue or pull-request templates.

### `.vscode/`

Contains shared Visual Studio Code settings and recommended extensions.

### `apps/api/`

Contains the FastAPI backend, domain objects, ingestion pipeline, persistence layer, repositories, migrations, scripts, and tests.

### `apps/web/`

Contains the Next.js web application.

### `docs/`

Contains product, architecture, engineering, governance, and source documentation.

### `docker-compose.yml`

Defines the local application services and their relationships.

### `Makefile`

Provides consistent commands for development, tests, linting, and Docker operations.

## API Structure

```text
apps/api/
├── alembic/
├── app/
│   ├── database/
│   ├── domain/
│   ├── ingestion/
│   ├── persistence/
│   ├── repositories/
│   └── main.py
├── scripts/
├── tests/
├── Dockerfile
├── pyproject.toml
├── pytest.ini
└── requirements.txt
```

### `app/domain/`

Contains framework-independent business concepts such as:

- `Organization`
- `Source`
- `Topic`
- `KnowledgeAsset`

Domain code must not import FastAPI, SQLAlchemy, HTTPX, feedparser, or other infrastructure frameworks.

### `app/ingestion/`

Contains the content collection and transformation pipeline.

Current flow:

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

### `app/persistence/`

Contains SQLAlchemy models and persistence-specific implementations.

Persistence code may depend on the domain. The domain must not depend on persistence.

### `app/repositories/`

Contains repository contracts used to retrieve and save domain objects.

Repository interfaces should describe application capabilities rather than exposing SQLAlchemy queries.

### `tests/`

Contains unit and integration tests.

All new behavior should include appropriate tests.

## Ingestion Concepts

### Source Adapter

A source adapter retrieves source-specific public content and returns `RawDocument` objects.

Examples include:

- RSS or Atom feeds
- HTML pages
- APIs
- GitHub releases
- PDFs
- Future public social sources

### Raw Document

A `RawDocument` preserves content and metadata as retrieved from the source.

It should not contain AI-generated or inferred information.

### Document Normalizer

A document normalizer converts a `RawDocument` into A11yDaily’s canonical `NormalizedDocument` format.

### Ingestion Pipeline

The ingestion pipeline runs normalized documents through ordered processing stages.

Each stage should have one clear responsibility.

### Knowledge Asset

A `KnowledgeAsset` is the canonical domain object representing a publicly available unit of accessibility knowledge.

A Knowledge Asset may represent an article, legal update, specification, release, webinar, PDF, research paper, podcast, video, or other public resource.

## Database Migrations

Alembic commands should normally run inside Docker because the hostname `postgres` resolves within the Docker network.

Generate a migration:

```bash
docker compose run --rm api \
  alembic revision --autogenerate -m "describe the migration"
```

Apply migrations:

```bash
docker compose run --rm api alembic upgrade head
```

Check the current migration:

```bash
docker compose run --rm api alembic current
```

## Git Workflow

Do not commit directly to `main`.

Create a focused branch:

```bash
git checkout -b <type>/<short-description>
```

Examples:

```text
feat/web-a11y-rss-source
fix/rss-date-parsing
docs/developer-onboarding
chore/dependency-maintenance
```

Before committing:

```bash
make api-lint
make api-test
git status
```

Commit messages should describe one logical change.

Examples:

```text
feat: add generic RSS source adapter
fix: preserve canonical URLs during normalization
docs: add developer onboarding guide
```

Push the branch and open a pull request.

## Pull Request Expectations

A pull request should:

- Solve one focused problem.
- Include tests for new or changed behavior.
- Pass linting and tests.
- Update documentation when behavior or architecture changes.
- Include an ADR when introducing a significant architectural decision.
- Avoid unrelated formatting or cleanup changes.
- Explain important tradeoffs or unresolved questions.

## Definition of Done

A change is complete when:

- The implementation is finished.
- Relevant tests pass.
- Linting passes.
- Error handling is appropriate.
- Type hints are present.
- Documentation is updated when needed.
- No generated files or secrets are committed.
- The pull request is reviewable and focused.

## Repository Hygiene

Do not commit:

- `.env`
- `.venv/`
- `.DS_Store`
- `node_modules/`
- `.next/`
- `__pycache__/`
- `.pytest_cache/`
- `.ruff_cache/`
- Local logs or temporary files

Before every commit:

```bash
git status
```

Confirm that only intentional files are staged.

## Suggested First Contribution

A good first contribution should be small, useful, and easy to verify.

Recommended examples:

- Improve an onboarding instruction discovered during setup.
- Add a focused unit test.
- Add a documented accessibility RSS source using the existing adapter.
- Improve error handling in a source adapter.
- Add structured logging to one ingestion component.
- Update an ADR or architecture diagram.

A first contribution should not require redesigning the ingestion pipeline, domain model, or persistence architecture.

## Troubleshooting

### Docker connection error

Example:

```text
Cannot connect to the Docker daemon
```

Start Docker Desktop and verify:

```bash
docker info
```

### Python interpreter cannot be resolved

Verify:

```bash
ls -l .venv/bin/python
```

Activate:

```bash
source .venv/bin/activate
```

Then select the interpreter in Visual Studio Code.

### Python cannot import `app`

Ensure:

```text
PYTHONPATH=/app
```

is configured for the API container and that the repository uses:

```text
apps/api/app/
```

for application code.

### PostgreSQL hostname cannot resolve locally

Inside Docker, use:

```text
postgres
```

From macOS, use:

```text
localhost
```

Run Alembic through Docker unless there is a specific reason not to.

### Tests report stale names after a rename

Clear generated caches:

```bash
rm -rf apps/api/.pytest_cache
rm -rf apps/api/.ruff_cache
find apps/api -type d -name "__pycache__" -prune -exec rm -rf {} +
find apps/api -type f -name "*.pyc" -delete
```

## Getting Help

Before asking for help:

1. Read the full error.
2. Confirm the current directory with `pwd`.
3. Check the active branch with `git status`.
4. Confirm Docker is running with `docker info`.
5. Confirm the virtual environment is active.
6. Run the smallest command that reproduces the problem.
7. Include the complete traceback or command output.

## Related Documents

- `README.md`
- `docs/VISION.md`
- `docs/CONSTITUTION.md`
- `docs/ARCHITECTURE.md`
- `docs/DOMAIN_MODEL.md`
- `docs/ENGINEERING.md`
- `docs/ROADMAP.md`
- `docs/adr/`
