from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import ConfigDict
from polyfactory.factories.pydantic_factory import ModelFactory
from app.core import Role
from app.core.auth import Authenticable
from app.core.jwt import Claims
from app.core.model import DataRequest
from app.domain.model.user import UserFilter

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Role = 0
        
    model_config = ConfigDict(from_attributes=True)
    
class UserProps(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
    
    model_config = ConfigDict(from_attributes=True)


class User(UserBase, Authenticable):
    id: int
    created_at: datetime = None
    
    class Config:
        from_attributes = True
        
    def get_claims(self) -> Claims :
        return Claims(sub = str(self.id))

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
        
    model_config = ConfigDict(from_attributes=True)
    
class UsersRequest(DataRequest[UserFilter]):
    filters : UserFilter = UserFilter

    
class UserRegisterFactory(ModelFactory[UserRegister]):
    __model__ = UserRegister
    
class UserBaseFactory(ModelFactory[UserBase]):
    __model__ = UserBase