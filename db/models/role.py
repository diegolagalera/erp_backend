from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    constant = Column(String,unique=True)
    created = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    disabled = Column(Boolean, default=False)
