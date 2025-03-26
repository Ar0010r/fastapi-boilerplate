from pydantic import BaseModel
from sqlalchemy import Select
from app.business.schema import User
from app.core.database.postgres.delete import DataEraser
from app.core.database.postgres.read import DataReader, DataScope
from app.core.database.postgres.write import DataWriter
from app.domain.model.user import User, UserFilter
from sqlalchemy.future import select
    
class UserReader(DataReader[User]):
    model = User
    
    async def find_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(self.model).filter(self.model.email == email)
        )
        return result.scalar_one_or_none()
    
    def filter(self, model: UserFilter) -> 'UserReader':
        if model.ids:
            self.query = self.query.filter(self.model.id.in_(model.ids))
            
        if model.roles:
            self.query = self.query.filter(self.model.role.in_(model.roles))
        
        if model.email:
            self.query = self.query.filter(self.model.email.ilike(f"%{model.email}%"))
            
        if model.name:
            self.query = self.query.filter(self.model.name.ilike(f"%{model.name}%"))
        
        return self
    
    def search(self, term: str) -> 'UserReader':
        if term:
            self.query = self.query.filter(
                self.model.name.ilike(f"%{term}%") | self.model.email.ilike(f"%{term}%")
            )
        
        return self
        
        
    
class UserWriter(DataWriter[User]):
    model = User

class UserEraser(DataEraser[User]):
    model = User

class UserScope(DataScope[User]):
    model = User
    
    def regular_scope(self, user: User) -> Select:
        return select(self.model).filter(self.model.id == user.id)
    
    
