from fastapi import FastAPI

app = FastAPI(title="{{cookiecutter.service_name}}")


@app.get("/health")
def health():
    return {"status": "ok"}
