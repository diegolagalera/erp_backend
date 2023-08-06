from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from db.models.user import user_roles
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    created = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    disabled = Column(Boolean, default=False)

    users = relationship('User', secondary=user_roles, back_populates='roles')

# OTHER RELATIONS


class UserInfo (BaseModel):
    id: int = None
    username: str = None

    class Config:
        orm_mode = True
# SCHEMAS
class RoleSchema(BaseModel):
    name: str
    created: datetime = datetime.now()
    disabled: Optional[bool] = False


class ShowRoleSchema(BaseModel):
    id: int
    name: str
    created: datetime = datetime.now()
    disabled: Optional[bool] = False
    users: Optional[List[UserInfo]] = None
    class Config:
        orm_mode = True


class ShowRoleSchemaPaginate(BaseModel):
    items: List[ShowRoleSchema] = []
    limit: int = None
    offset: int = None
    total:int = None

    class Config:
        orm_mode = True


class UpdateRoleSchema(BaseModel):
    name: str = None
    created: Optional[datetime] = None
    disabled: Optional[bool] = False


# ESQUEMAS PARA EL INPUT DE FILTER
class filterRoleParamsSchema(BaseModel):
    name: Union[str, List[str]] = None
    disabled: Union[str, bool] = None
    text: Union[str, List[str]] = None
    limit: int = None
    offset: int = None
    type: str = None


class filter(BaseModel):
    params: List[filterRoleParamsSchema]
