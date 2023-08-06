from datetime import datetime
from typing import Optional
from datetime import datetime
from config.database import Base
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String)
    province = Column(String)
    city = Column(String)
    postal_code = Column(String)
    others = Column(String)
    created = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='addresses')

class AddressSchema(BaseModel):
    street: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    others: Optional[str] = None

class ShowAddressSchema(BaseModel):
    id: int
    street: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    others: Optional[str] = None

    class Config:
        orm_mode = True

class UpdateAddressSchema(BaseModel):
    id: int
    street: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    others: Optional[str] = None