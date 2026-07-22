from fastapi import FastAPI

from app.api.routes.knowledge_assets import (
    router as knowledge_assets_router,
)
from app.logging_config import configure_logging

configure_logging()

app = FastAPI(title="A11yDaily API")

app.include_router(knowledge_assets_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "A11yDaily API",
    }
