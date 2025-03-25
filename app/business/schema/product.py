from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.core.model import DataRequest


class ProductFilter(BaseModel):
    ids: list[int] = []
    name: Optional[str] = None
    description: Optional[str] = None
    statuses: list[int] = []
    price_from: Optional[int] = None
    price_to: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class ProductRequest(DataRequest[ProductFilter]):
    filters : ProductFilter = ProductFilter