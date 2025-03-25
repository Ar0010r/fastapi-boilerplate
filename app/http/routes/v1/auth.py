from fastapi import APIRouter, Depends
from injector import Injector

from app.business.action import auth as action
from app.business.schema.user import User, UserBase, UserProps, UserRegister
from app.core.model import Credentials
from app.http.routes import Route
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(route_class=Route)

@router.post("/register", response_model=str)
async def create(model: UserRegister) -> str:
    return await action.register(model)

@router.post("/login", response_model=str)
async def login(model: Credentials) -> str:
    return await action.login(model)

@router.get("/auth-user", response_model=User)
async def get_auth_user(user: User = Depends(action.get_user)):
    return user