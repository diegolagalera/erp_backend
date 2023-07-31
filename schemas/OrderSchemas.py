from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class OrderSchema(BaseModel):
    # id: Optional[int] = None
    status: Optional[str] = "PENDING"
    quantity: int
    user_id: Optional[int] = None

    class config:
        orm_mode = True


class ShowOrderSchema(BaseModel):
    id: int
    status: str
    quantity: int
    user_id: Optional[int] = None

    class config:
        orm_mode = True


class ShowOrderSchemaPaginate(BaseModel):
    items: List[ShowOrderSchema] = []
    limit: int = None
    offset: int = None

    class Config:
        orm_mode = True


class UpdateOrderSchema(BaseModel):
    # id: int = None
    status: str = None
    quantity: int = None
    user_id: Optional[int] = None
   


class filterUserParamsSchema(BaseModel):
    status: Union[str, List[str]] = None
    quantity: Union[str, List[str]] = None
    user_id: Union[int, List[int]] = None
    text: Union[str, List[str]] = None
    limit: int = None
    offset: int = None
    type: str = None


class filter(BaseModel):
    params: List[filterUserParamsSchema]
