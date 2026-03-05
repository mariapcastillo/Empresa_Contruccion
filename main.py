from fastapi import FastAPI
from db.database import test_db_connection
from routes import operarios_routes
from routes import notificaciones_operario, notificaciones_admin
from routes import obras_routes
from routes import auth_routes

app = FastAPI()

@app.get("/")
async def root():
    return {"ok": True}

@app.get("/health")
async def health():
    await test_db_connection()
    return {"api": "ok", "db": "ok"}


app.include_router(obras_routes.router, prefix='/obras', tags=['obras'])

app.include_router(operarios_routes.router, prefix='/operarios', tags= ['operarios'])

app.include_router(notificaciones_operario.router, prefix='/operarios', tags=['notificaciones'])

app.include_router(notificaciones_admin.router, prefix='/admin', tags=['notificaciones'])

app.include_router(auth_routes.router, prefix='/auth', tags=['auth'])