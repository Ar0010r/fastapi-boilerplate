from typing import Generic, TypeVar
from sqlalchemy.orm import DeclarativeMeta
from pydantic import BaseModel
from abc import ABC, abstractmethod
from app.core.database.postgres.write import DataWriter

TModel = TypeVar('TModel', bound=DeclarativeMeta)

class IService(ABC, Generic[TModel]):
    @abstractmethod
    async def create(self, schema: BaseModel)->int:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, schema: BaseModel) -> bool:
        raise NotImplementedError
        
    @abstractmethod
    async def modify(self, schema: BaseModel) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def edit(self, original: BaseModel, update_with:BaseModel) -> bool:
        raise NotImplementedError


class BaseService(IService[TModel]):
    model: TModel
    repository: DataWriter[TModel]
        
    async def create(self, schema: BaseModel)->int:
        data = schema.model_dump()
        model = self.model(**data)

        return await self.repository.create(model)
    
    async def update(self, schema: BaseModel) -> bool:
        data = schema.model_dump()
        model = self.model(**data)
            
        result = await self.repository.update(model)
        
        return isinstance(result, self.model)
        
        
    async def modify(self, schema: BaseModel) -> int:
        if schema.id is None:
            raise Exception('Model ID is required')
        
        id = schema.id
        data = schema.model_dump(exclude_unset=True)
        data.pop('id', None)
        
        return await self.repository.modify(id, data)
    
    
    async def edit(self, original: BaseModel, update_with:BaseModel) -> bool:
        data = update_with.model_dump(exclude_unset=True, exclude={"id"})
        
        for key, value in data.items():
            setattr(original, key, value)
            
        return await self.update(original)
        
        
    # async def update(self, id: int, schema: BaseModel):
    #     model = await self.repository.find_or_fail(id)
    #     for key, value in schema.model_dump().items():
    #         setattr(model, key, value)
            
    #     await self.repository.update(model)
    
    async def store(self, schema: BaseModel)->int:
        if schema.id is int:
           return await self.update(schema.id, schema)

        return await self.create(schema)
    
