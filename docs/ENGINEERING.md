Volume 7: Engineering Standards
Git Workflow
main
develop
feature/_
fix/_
docs/\*
Commit Style
feat: add RSS ingestion framework
fix: prevent duplicate intelligence items
docs: update architecture blueprint
test: add API health check tests
chore: configure Docker services
Quality Gates
Every feature should include:
implementation
tests
documentation update
accessibility review when UI changes
linting and formatting
Code Standards
Frontend:
TypeScript
ESLint
Prettier
semantic HTML
accessible React components
Backend:
Python
FastAPI
SQLAlchemy
Alembic
Ruff
Black
pytest
Definition of Done
A feature is done when:
it runs locally
tests pass
documentation is updated
no known accessibility blockers exist
it can be explained clearly in the roadmap
