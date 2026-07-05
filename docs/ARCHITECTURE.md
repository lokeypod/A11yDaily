Volume 2: System Architecture
A11yDaily uses a modular service architecture.
Core Services
Web App: Next.js user interface
API Service: FastAPI backend
Worker Service: background processing
Database: PostgreSQL with pgvector
Queue: Redis
AI Layer: summarization, tagging, clustering, embeddings
Source Registry: list of trusted sources and ingestion settings
Data Flow
Source Registry
↓
Connector
↓
Raw Intelligence Item
↓
Queue
↓
Content Extraction
↓
AI Enrichment
↓
Deduplication / Clustering
↓
PostgreSQL + pgvector
↓
API
↓
Web App
Local Development
docker compose up
Runs:
web
api
worker
postgres
redis
