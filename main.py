from fastapi import FastAPI
from db.database import test_db_connection
from routes import operarios_routes
from routes import notificaciones_operario, notificaciones_admin
from routes import obras_routes
from routes import auth_routes
from routes import foto_admin_routes, foto_operario_routes
from routes import me_routes

app = FastAPI()

@app.get("/")
async def root():
    return {"ok": True}

@app.get("/health")
async def health():
    await test_db_connection()
    return {"api": "ok", "db": "ok"}


# Auth
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

# Admin
app.include_router(obras_routes.router, prefix="/admin/obras", tags=["admin-obras"])
app.include_router(operarios_routes.router, prefix="/admin/operarios", tags=["admin-operarios"])
app.include_router(notificaciones_admin.router, prefix="/admin", tags=["admin-notificaciones"])

# Operario
app.include_router(notificaciones_operario.router, prefix="/operarios", tags=["operario-notificaciones"])


app.include_router(foto_admin_routes.router, prefix="/admin/obras", tags=["admin-fotos"])
app.include_router(foto_operario_routes.router, prefix="/operarios", tags=["operario-fotos"])

app.include_router(me_routes.router, tags=["me"])