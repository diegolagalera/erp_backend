from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    direccion = Column(String)
    telefono = Column(Integer)
    correo = Column(String, unique=True)
    creacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    estado= Column(Boolean, default=False)
    
