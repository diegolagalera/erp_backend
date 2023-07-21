from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    username:str
    password:str
    nombre:str
    apellido:str
    direccion: Optional[str]
    telefono:int
    correo:str
    creacion:datetime=datetime.now()

class UserId(BaseModel):
    id:int

class showUser(BaseModel):
    username:str
    nombre:str
    apellido:str
    telefono:int
    # PARA QUE NO DE INTERNAL SERVER ERRO TENEMOS QUE PONER orm_mode true
    class Config(): 
        orm_mode = True

class UpdateUser(BaseModel):
    username:str = None
    password:str = None
    nombre:str = None
    apellido:str = None
    direccion:str = None
    telefono:int = None
    correo:str = None
