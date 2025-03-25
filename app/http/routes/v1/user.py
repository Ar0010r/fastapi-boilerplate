from fastapi import APIRouter, Depends

from app.business.action import user as action
from app.business.action import auth
from app.business.schema.user import User, UserProps, UserRegister, UsersRequest
from app.core.model import DataList
from app.http.routes import Route

router = APIRouter(route_class=Route)

# @router.post("/user", response_model=User)
# async def create(model: UserRegister, user: User = Depends(auth.get_user)) -> User:
#     return await action.create(model)

@router.put("/user/{id}", response_model=User)
async def update(id: int, model: UserProps, user: User = Depends(auth.get_user)) -> User:
    return await action.update(id, model, user)

@router.delete("/user/{id}", response_model=int)
async def delete(id: int, user: User = Depends(auth.get_user)):
    return await action.delete(id, user)

@router.get("/user/{id}", response_model=User)
async def show(id: int, user: User = Depends(auth.get_user)):
    return await action.show(id, user)

@router.get("/user", response_model=DataList[User])
async def list(request: UsersRequest = Depends(), user: User = Depends(auth.get_user)):
    return await action.list(request, user)
