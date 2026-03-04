from fastapi import FastAPI
from db.database import test_db_connection
from routes import operarios_routes
from routes import notificaciones_operario

app = FastAPI()

@app.get("/")
async def root():
    return {"ok": True}

@app.get("/health")
async def health():
    await test_db_connection()
    return {"api": "ok", "db": "ok"}




app.include_router(operarios_routes.router, prefix='/operarios', tags= ['operarios'])

app.include_router(notificaciones_operario.router, prefix='/operarios', tags=['notificaciones'])