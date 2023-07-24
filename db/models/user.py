from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    direccion = Column(String)
    telefono = Column(Integer)
    email = Column(String, unique=True)
    creacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    disabled = Column(Boolean, default=False)
    role = Column(PG_ARRAY(Integer), server_default='{1,2}')
    # role = Column(PG_ARRAY(int), server_default='{"1","2"}')
    # role = Column(PG_ARRAY(String), default=["user"])
    orders = relationship('Order', back_populates='user')