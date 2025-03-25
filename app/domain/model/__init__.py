from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Float, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.sql import func
from app.core.database.postgres import Base


@dataclass
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    description = Column(String)
    price = Column(Integer, default=0)
    status = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    



    
#created_at = Column(DateTime, default=datetime.now(timezone.utc))