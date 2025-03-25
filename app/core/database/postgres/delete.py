from pydantic import BaseModel
from sqlalchemy.future import select
from typing import Callable, Generic, Type, TypeVar, overload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_async_sqlalchemy import db
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import delete

T = TypeVar('T', bound=DeclarativeMeta)


class DataEraser(Generic[T]):
    model: T = T

    def __init__(
            self, session_or_factory: AsyncSession | Callable[[], AsyncSession] = None
    ) -> None:
        #self.model = T
        self._session_or_factory = session_or_factory

    @property
    def session(self) -> AsyncSession:
        if self._session_or_factory is None:
            self._session_or_factory = db.session
        if isinstance(self._session_or_factory, AsyncSession):
            return self._session_or_factory
        return self._session_or_factory()

    @overload
    async def delete(self, id: int) -> int:
        ...
    
    @overload
    async def delete(self, model: T) -> int:
        ...
    
    @overload
    async def delete(self, model: BaseModel) -> int:
        ...
        
        
    async def delete(self, model: T | BaseModel | int) -> int:
        id = None
        
        if isinstance(model, BaseModel):
            id = model.id
        
        if isinstance(model, int):
            id = model
        
        if isinstance(model, self.model):
            id = model.id
        
        if id is None or id == 0:
            return 0
        
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        
        return result.rowcount
    
    
    async def delete_many(self, ids: list[int]) -> int:
        stmt = delete(self.model).where(self.model.id.in_(ids))
        result = await self.session.execute(stmt)
        await self.session.flush()
        
        return result.rowcount
    
