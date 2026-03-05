from fastapi import APIRouter
from models.auth_model import RegisterRequest, LoginRequest, TokenResponse
from controllers.auth_controller import register_user, login_user

router = APIRouter()

@router.post("/register", status_code=201)
async def register(data: RegisterRequest):
    return await register_user(data)

@router.post("/login", response_model=TokenResponse, status_code=200)
async def login(data: LoginRequest):
    return await login_user(data)