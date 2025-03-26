from typing import Any, List
from pydantic import BaseModel, EmailStr, StrictInt
from typing import Generic, TypeVar

T = TypeVar('T')

class Filter(BaseModel, Generic[T]):
    field : str
    operation : str = 'eq'
    value : T

class OrderBy(BaseModel):
    field : str
    direction : str = 'asc'

class PageRequest(BaseModel):
    page : int = 1
    per_page : int = 10

class ChunkRequest(BaseModel):
    skip : int = 0
    take : int = 10
    
class DataRequest(BaseModel, Generic[T]):
    filters : T = T
    order_by : OrderBy = None
    pagination : PageRequest = None
    search_term : str = None

class DataList(BaseModel, Generic[T]):
    rows : StrictInt = 0
    data : List[T] = []
    
    def is_empty(self) -> bool:
        return self.rows == 0
    
    def count(self) -> int:
        return len(self.data)
    
    class Config:
        arbitrary_types_allowed = True
        
class Credentials(BaseModel):
    email: EmailStr
    password: str