from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class UserSchema(BaseModel):
    username: str
    password: str
    nombre: str
    apellido: str
    direccion: Optional[str]
    telefono: int
    email: str
    creacion: datetime = datetime.now()
    role: List[int] = None

    class config:
        orm_mode = True


class ShowUserSchema(BaseModel):
    id: int
    username: str
    nombre: str
    apellido: str
    telefono: int
    creacion: datetime
    role: List[int]
    class Config:
        orm_mode = True


class ShowUserSchemaPaginate(BaseModel):
    items: List[ShowUserSchema] = []
    limit: int = None
    offset: int = None
    class Config:
        orm_mode = True


class UpdateUserSchema(BaseModel):
    id:int
    username: str = None
    password: str = None
    nombre: str = None
    apellido: str = None
    direccion: str = None
    telefono: int = None
    role: List[int] = None
    email: str = None


class filterUserParamsSchema(BaseModel):
    # id:int
    username: Union[str, List[str]] = None
    nombre: Union[str, List[str]] = None
    apellido: Union[str, List[str]] = None
    telefono: Union[int, List[int]] = None
    creacion: List[Union[datetime, None]] = None
    email: Union[str, List[str]] = None
    disabled: Union[str, bool] = None
    text: Union[str, List[str]] = None
    limit: int = None
    offset: int = None
    type: str = None


class filter(BaseModel):
    params: List[filterUserParamsSchema]
# class UserId(BaseModel):
#     id:int
