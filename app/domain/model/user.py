from dataclasses import dataclass
from typing import Optional
from faker import Faker
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.sql import func
from app.core import IntEnum, Role
from app.core.database.postgres import Base
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.orm import DeclarativeMeta

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    role = Column(IntEnum(Role), default=Role.REGULAR.value)
    # role = Column(Enum(Role, values_callable=get_enum_values), default=Role.REGULAR.value)
    name = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    
fake = Faker()

# class SQLAlchemyModelFactory(SQLAlchemyFactory):
#     """Custom base factory for SQLAlchemy models."""
    
#     @classmethod
#     def get_model(cls) -> DeclarativeMeta:
#         return cls.__model__
    
class UserFactory():
    
    @staticmethod
    def build():
        return User(
            email = fake.email(),
            name = fake.name(),
            role = Role.REGULAR,
            password = fake.password(),
            created_at = fake.date_time_this_year()
        )
    
    
    
user_factory = UserFactory()
    
class UserFilter(BaseModel):
    ids: list[int] = []
    name: Optional[str] = None
    email: Optional[str] = None
    roles: list[Role] = []
        
    model_config = ConfigDict(from_attributes=True)