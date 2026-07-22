from fastapi import FastAPI

from app.logging_config import configure_logging

configure_logging()

app = FastAPI(title="A11yDaily API")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "A11yDaily API",
    }
