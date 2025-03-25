from sqlalchemy.future import select
from typing import Callable, Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_async_sqlalchemy import db
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import update
from abc import ABC, abstractmethod

T = TypeVar('T', bound=DeclarativeMeta)

class IDataWriter(ABC, Generic[T]):
    @abstractmethod
    async def create(self, model: T) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update(self, model: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def modify(self, id: int, params: dict) -> int:
        raise NotImplementedError

class DataWriter(IDataWriter[T]):
    model: T = T

    def __init__(
            self, session_or_factory: AsyncSession | Callable[[], AsyncSession] = None
    ) -> None:
        self._session_or_factory = session_or_factory

    @property
    def session(self) -> AsyncSession:
        if self._session_or_factory is None:
            self._session_or_factory = db.session
        if isinstance(self._session_or_factory, AsyncSession):
            return self._session_or_factory
        return self._session_or_factory()

    async def create(self, model: T) -> int:
        self.session.add(model)
        await self.session.flush()
        return model.id
    
    # async def update(self, model: T) -> None:   
    #     if model.id is None:
    #         raise Exception('Model ID is required')
        
    #     values = model.dict(exclude_unset=True)
    #     update_stmt = update(self.model).where(self.model.id == model.id).values(values)
    #     a = await self.session.execute(update_stmt)
        
        # self.model.update().where(self.model.id == model.id).values(model)

    async def update(self, model: T) -> T:
        result = await self.session.merge(model)
        await self.session.flush()
        
        return result
        
    async def modify(self, id: int, params: dict) -> int:
        stmt = update(self.model).where(self.model.id == id).values(params)
        result = await self.session.execute(stmt)
        
        await self.session.flush()
        
        return result.rowcount
