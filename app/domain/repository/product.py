from sqlalchemy import Select
from app.business.schema import User
from app.business.schema.product import ProductFilter
from app.core.database.postgres.delete import DataEraser
from app.core.database.postgres.read import DataReader, DataScope
from app.core.database.postgres.write import DataWriter
from app.domain.model import Product
from sqlalchemy.future import select
    
class ProductReader(DataReader[Product]):
    model = Product
    
    def filter(self, model: ProductFilter) -> 'ProductReader':
        if model.ids:
            self.query = self.query.filter(self.model.id.in_(model.ids))
            
        if model.name:
            self.query = self.query.filter(self.model.name.ilike(f"%{model.name}%"))
        
        if model.description:
            self.query = self.query.filter(self.model.description.ilike(f"%{model.description}%"))
        
        if model.price_from:
            self.query = self.query.filter(self.model.price >= model.price_from)
        
        if model.price_to:
            self.query = self.query.filter(self.model.price <= model.price_to)
        
        if model.statuses:
            self.query = self.query.filter(self.model.category.in_(model.statuses))
        
        return self
    
class ProductWriter(DataWriter[Product]):
    model = Product

class ProductEraser(DataEraser[Product]):
    model = Product

class ProductScope(DataScope[Product]):
    model = Product
    
    def regular_scope(self, user: User) -> Select:
        return select(self.model).filter(
            (self.model.user_id == user.id) | (self.model.status > 0)
        )
    
