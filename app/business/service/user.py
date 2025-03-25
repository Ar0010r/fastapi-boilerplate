from fastapi import Depends
from app.business.schema.user import UserBase, UserRegister
from app.business.service import BaseService, IService
from app.core.hashing.bcrypt import Bcrypt
from app.domain.model.user import User
from app.domain.repository.user import UserWriter
from injector import inject

class IUserService(IService[User]):
    pass

class UserService(IUserService, BaseService[User]):
    
    @inject
    def __init__(self, repository: UserWriter):
        self.model = User
        self.repository = repository
        
    async def create(self, model: UserRegister) -> int:
        model.password = Bcrypt.hash_once(model.password)
        return await super().create(model)