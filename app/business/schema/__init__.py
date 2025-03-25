from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import ConfigDict
from polyfactory.factories.pydantic_factory import ModelFactory

from app.core import Role

class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    name: str
    password: Optional[str] = None


class User(UserCreate):
    id: int
    role: Role 
    created_at: datetime
    

class ProductBase(BaseModel):
    name: str
    description: str
    price: int = 0
    status: int = 0
        
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    user_id: int
    name: str
    description: str
    price: int = 0
    
    class Config:
        from_attributes = True
        
class ProductInit(BaseModel):
    name: str
    description: str
    price: int = 0
    
    class Config:
        from_attributes = True
    
    
class ProductBaseFactory(ModelFactory[ProductBase]):
    __model__ = ProductBase
    
class ProductCreateFactory(ModelFactory[ProductCreate]):
    __model__ = ProductCreate
    
class ProductInitFactory(ModelFactory[ProductInit]):
    __model__ = ProductInit
        
    
class ProductProps(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    status: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class Product(ProductBase):
    id: int
    user_id: int
    created_at: datetime = None
    
    class Config:
        from_attributes = True


