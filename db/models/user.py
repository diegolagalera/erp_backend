from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
# from db.models.role import Role
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import List, Union

user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', Integer, ForeignKey('users.id')),
                   Column('role_id', Integer, ForeignKey('roles.id'))
                   )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    direction = Column(String)
    tel = Column(Integer)
    email = Column(String, unique=True)
    created = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    disabled = Column(Boolean, default=False)

    orders = relationship('Order', back_populates='user')

    roles = relationship('Role', secondary=user_roles, back_populates='users')

# OTHER RELATIONS


class RolesInfo (BaseModel):
    id: int = None
    name: str = None

    class Config:
        orm_mode = True
# SCHEMAS


class UserSchema(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    surname: Optional[str] = None
    direction: Optional[str] = None
    tel: int
    email: str
    created: Optional[datetime] = datetime.now()
    disabled: Optional[bool] = False
    roles: Optional[List[int]] = None


class ShowUserSchema(BaseModel):
    id: int
    username: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    direction: Optional[str] = None
    tel: int
    email: str
    created: datetime
    disabled: bool
    roles: Optional[List[RolesInfo]] = None

    class Config:
        orm_mode = True


class ShowUserSchemaPaginate(BaseModel):
    items: List[ShowUserSchema] = []
    limit: int = None
    offset: int = None
    total: int = None

    class Config:
        orm_mode = True


class UpdateUserSchema(BaseModel):
    username: str = None
    password: str = None
    name: str = None
    surname: str = None
    direction: str = None
    tel: int = None
    email: str = None
    disabled: bool = None
    roles: Optional[List[int]] = None

    # role: List[int] = None


class filterUserParamsSchema(BaseModel):
    # id:int
    username: Union[str, List[str]] = None
    name: Union[str, List[str]] = None
    surname: Union[str, List[str]] = None
    direction: Union[str, List[str]] = None
    tel: Union[int, List[int]] = None
    email: Union[str, List[str]] = None
    created: List[Union[datetime, None]] = None
    disabled: Union[str, bool] = None
    text: Union[str, List[str]] = None
    limit: int = None
    offset: int = None
    type: str = None


class filter(BaseModel):
    params: List[filterUserParamsSchema]
