from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar
from sqlalchemy.orm import DeclarativeMeta
from pydantic import BaseModel
from app.business.schema.user import User
from app.business.service import BaseService, IService
from app.core.database.postgres.read import IReader

TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse', bound=BaseModel)
TModel = TypeVar('TModel', bound=DeclarativeMeta)

class CreateCommand(ABC, Generic[TRequest, TResponse, TModel]):
    return_model: Type[TResponse]
    
    def __init__(self, service: IService[TModel], reader: IReader[TModel]):
        self.service = service
        self.reader = reader
    
    async def execute(self, request: TRequest, user: Optional[User] = None) -> TResponse:
        id = await self.service.create(request)
        model = await self.reader.find_or_fail(id)
        
        return self.return_model.model_validate(model)
    
class UpdateCommand(ABC, Generic[TRequest, TResponse]):
    service: IService[TModel]
    reader: IReader[TModel]
    
    @abstractmethod
    async def execute(self, id: int, request: TRequest, user: User) -> TResponse:
        id = await self.service.create(request)
        model = await self.reader.find_or_fail(id)
        
        return TResponse.model_validate(model)
        
        