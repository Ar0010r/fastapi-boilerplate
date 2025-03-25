from fastapi import Depends
from injector import Injector
from app.business.action.user import get_by_creds, get_by_token
from app.business.schema.user import UserRegister
from app.core import auth
from app.business.service.user import UserService
from app.core.model import Credentials

injector = Injector()
service = injector.get(UserService)

async def register(model: UserRegister) -> str:
    creds = Credentials(email=model.email, password=model.password)
    await service.create(model)
    
    return await login(creds)

async def login(creds: Credentials) -> str:
    user = await get_by_creds(creds)
    
    return auth.issue_token(user)

async def get_user(token: str = Depends(auth.get_token)):
    return await get_by_token(token)


#  иденпотентность
#  yроавни изоляции транзацкий