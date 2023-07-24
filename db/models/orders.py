from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user= relationship('User',back_populates='orders')