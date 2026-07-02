from fastapi import FastAPI

app = FastAPI(title="risk-scoring-service")


@app.get("/health")
def health():
    return {"status": "ok"}
