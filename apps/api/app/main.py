from fastapi import FastAPI

app = FastAPI(title="A11yDaily API", version="0.1.0")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "A11yDaily API",
        "version": "0.1.0"
    }
