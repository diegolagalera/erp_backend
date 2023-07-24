from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class OrderSchema(BaseModel):
    id: Optional[int] = None
    status: Optional[str] = "PENDING"
    quantity: int
    user_id: Optional[int] = None

    class config:
        orm_mode = True


class ShowOrderSchema(BaseModel):
    id: int
    status: str
    quantity: int
    user_id: int

    class config:
        orm_mode = True


# class ShowUserSchemaPaginate(BaseModel):
#     items: List[ShowUserSchema] = []
#     limit: int = None
#     offset: int = None
#     role: List[int] = None

#     class Config:
#         orm_mode = True


class UpdateOrderSchema(BaseModel):
    id: int = None
    status: str = None
    quantity: int = None
    user_id: int = None
   


# class filterUserParamsSchema(BaseModel):
#     username: Union[str, List[str]] = None
#     nombre: Union[str, List[str]] = None
#     apellido: Union[str, List[str]] = None
#     telefono: Union[int, List[int]] = None
#     creacion: List[Union[datetime, None]] = None
#     email: Union[str, List[str]] = None
#     disabled: Union[str, bool] = None
#     text: Union[str, List[str]] = None
#     limit: int = None
#     offset: int = None
#     type: str = None


# class filter(BaseModel):
#     params: List[filterUserParamsSchema]
