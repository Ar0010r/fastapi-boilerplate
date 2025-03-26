from fastapi import APIRouter, Depends
from app.business.action import auth
from app.business.action import product as action
from app.business.schema import Product, ProductBase, ProductProps
from app.business.schema.user import User
from app.http.routes import Route

router = APIRouter(route_class=Route)

@router.post("/product", response_model=Product)
async def create(model: ProductBase, user: User = Depends(auth.get_user)) -> Product:
    return await action.create(model, user)

@router.put("/product/{id}", response_model=Product)
async def update(id: int, model: ProductProps, user: User = Depends(auth.get_user)) -> Product:
    return await action.update(id, model, user)

@router.delete("/product/{id}", response_model=int)
async def delete(id: int, user: User = Depends(auth.get_user)):
    return await action.delete(id, user)

@router.get("/product/{id}", response_model=Product)
async def show(id: int, user: User = Depends(auth.get_user)):
    return await action.show(id, user)
