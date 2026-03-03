from fastapi import FastAPI
from db.database import test_db_connection

app = FastAPI()

@app.get("/")
async def root():
    return {"ok": True}

@app.get("/health")
async def health():
    await test_db_connection()
    return {"api": "ok", "db": "ok"}