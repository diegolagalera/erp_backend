from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    nombre: str
    apellido: str
    direccion: Optional[str]
    telefono: int
    correo: str
    creacion: datetime = datetime.now()


class ShowUserSchema(BaseModel):
    username: str
    nombre: str
    apellido: str
    telefono: int

    class Config():
        orm_mode = True


class UpdateUserSchema(BaseModel):
    username: str = None
    password: str = None
    nombre: str = None
    apellido: str = None
    direccion: str = None
    telefono: int = None
    correo: str = None

# class UserId(BaseModel):
#     id:int
