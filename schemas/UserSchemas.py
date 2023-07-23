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
    correo: str
    creacion: datetime = datetime.now()


class ShowUserSchema(BaseModel):
    username: str
    nombre: str
    apellido: str
    telefono: int
    creacion: datetime
    class Config():
        orm_mode = True

class ShowUserSchemaPaginate(BaseModel):
    items:List[ShowUserSchema] = []
    limit: str = None
    offset: str = None

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

class username(BaseModel):
    username: Union[str, List[str]] = None
    type: str= None


class filterUserParamsSchema(BaseModel):
    username: Union[str, List[str]] = None
    nombre: Union[str, List[str]] = None
    apellido: Union[str, List[str]] = None
    telefono: Union[int, List[int]] = None
    creacion: List[Union[datetime, None]] =None
    correo: Union[str, List[str]] = None
    disabled: Union[str, bool] = None
    text: Union[str, List[str]] = None
    limit: int = None
    offset: int = None
    type: str= None



class filter(BaseModel):
    params: List[filterUserParamsSchema]
# class UserId(BaseModel):
#     id:int
