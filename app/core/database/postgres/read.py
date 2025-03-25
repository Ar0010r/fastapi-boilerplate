from pydantic import BaseModel
from sqlalchemy import Select, Tuple, func
from sqlalchemy.future import select
from typing import Callable, Generic, List, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_async_sqlalchemy import db
from sqlalchemy.orm import DeclarativeMeta

from app.business.schema import User
from app.core import Role
from app.core.model import ChunkRequest, DataList, Filter, OrderBy, PageRequest

T = TypeVar('T', bound=DeclarativeMeta)

TDto = TypeVar("TDto", bound=BaseModel)

class IReader(Generic[T]):
    async def find(self, id: int) -> T | None:
        raise NotImplementedError

    async def find_or_fail(self, id: int) -> T:
        raise NotImplementedError

    async def find_many(self, ids: list[int]) -> list[T]:
        raise NotImplementedError

    def set_scope(self, query: Select) -> 'IReader[T]':
        raise NotImplementedError

    def order_by(self, request: OrderBy | None) -> 'IReader[T]':
        raise NotImplementedError

    def filter_id(self, value: int | list[int]) -> 'IReader[T]':
        raise NotImplementedError

    async def chunk(self, request: ChunkRequest) -> DataList[T]:
        raise NotImplementedError

    async def paginate(self, request: PageRequest | None) -> DataList[T]:
        raise NotImplementedError

    async def first(self) -> T | None:
        raise NotImplementedError

    async def first_or_fail(self) -> T:
        raise NotImplementedError


class DataReader(IReader[T]):
    model : T = T

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
    
    async def find(self, id: int) -> T | None:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def find_or_fail(self, id: int) -> T:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == id)
        )
        return result.scalar_one()
    
    async def find_many(self, ids: list[int]) -> list[T]:
        return await self.session.execute(
            select(self.model).filter(self.model.id.in_(ids))
        ).scalars().all()
    
    def set_scope(self, query: Select) -> 'DataReader[T]':
        self.query = query
        return self
    
    def order_by(self, request: OrderBy | None) -> 'DataReader[T]':
        if not isinstance(request, OrderBy):
            return self
        
        expr = db.text(request.field);
        
        if request.direction == 'desc':
            expr = expr.desc()
        
        self.query = self.query.order_by(expr)
            
        return self
    
    def filter_id(self, value: int|list[int]) -> 'DataReader[T]':
        if isinstance(value, list):
            self.query = self.query.filter(self.model.id.in_(value))
        
        if isinstance(value, int):
            self.query = self.query.filter(self.model.id == value)
        
        return self
    
    async def chunk(self, request: ChunkRequest) -> DataList[T]:
        count = await self.session.execute(
                select(func.count()).select_from(self.query.subquery())
            )
        
        self.query = self.query.limit(request.take).offset(request.skip)
        items = await self.session.execute(self.query)
        
        return DataList(rows=count.scalars().one(), data=items.scalars().all())
    
    # async def chunk(self, request: ChunkRequest) -> DataList[T]:
    #     self.query = self.query.limit(request.take).offset(request.skip)
        
    #     a = await self.session.execute(self.query)
        
    #     return DataList(rows=a.scalars().count(), data=a.scalars().all())
        
    async def paginate(self, request: PageRequest | None) -> DataList[T]:
        if not isinstance(request, PageRequest):
            request = PageRequest()
            
        skip = (request.page - 1) * request.per_page
        request = ChunkRequest(skip=skip, take=request.per_page)
        
        return await self.chunk(request)
    
    async def first(self) -> T | None:
        r = await self.session.execute(self.query)
        return r.scalar_one_or_none()
    
    async def first_or_fail(self) -> T:
        r = await self.session.execute(self.query)
        return r.scalar_one()
    
       
    
class DataScope(Generic[T]):
    model: T = T
    
    def get(self, user: User) -> Select:
        if user.role == Role.ADMIN:
            return self.admin_scope(user)
        
        return self.regular_scope(user)
    
    def admin_scope(self, user: User) -> Select:
        return select(self.model)
    
    def regular_scope(self, user: User) -> Select:
        return self.admin_scope()
    
    