from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Lyrics Semantic Search API", version="0.1.0")
app.include_router(router)

# root health-check
@app.get("/")
def read_root():
    return {"status": "ok"}