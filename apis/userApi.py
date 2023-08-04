from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from db.models.user import filter, UserSchema, ShowUserSchema, UpdateUserSchema, ShowUserSchemaPaginate, filterUserParamsSchema
from service.userService import UserService
from config.roleChecker import RoleChecker
from config.roleConstant import ROLES
from fastapi.encoders import jsonable_encoder
from dateutil.parser import parse as parse_datetime
from config.database import db_connection
from sqlalchemy.orm import Session

userApi = APIRouter(
    prefix='/user', tags=["user"], responses={404: {"message": "NO FOUND ROUTA /user"}})

acces_get_ussers = [ROLES['admin'], ROLES['user']]
acces_get_usser = [ROLES['admin']]
acces_create_user = [ROLES['admin']]
acces_update_user = [ROLES['admin'], ROLES['user']]
acces_delete_user = [ROLES['admin'], ]

# @userApi.post("/", response_model=ShowUserSchemaPaginate)


@userApi.post("/", response_model=ShowUserSchemaPaginate, dependencies=[Depends(RoleChecker(acces_get_ussers))])
def get_users(filter_paginate: filter = None, db: Session = Depends(db_connection)):
    userService = UserService(db=db)
    # quita todos los valores NONES del filtro
    filter = filter_paginate.dict(exclude_unset=True)
    items, limit, offset, total = userService.get_items(filter['params'])
    response = ShowUserSchemaPaginate()
    response.items = items
    response.limit = limit
    response.offset = offset
    response.total = total
    return response


@userApi.get("/{user_id}", response_model=ShowUserSchema, dependencies=[Depends(RoleChecker(acces_get_usser))])
def get_user(user_id: int, db: Session = Depends(db_connection)):
    userService = UserService(db=db)
    return userService.get_item(user_id)


@userApi.post("/create", response_model=ShowUserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema, db: Session = Depends(db_connection)):
    userService = UserService(db=db)
    return userService.create_item(user)


@userApi.patch("/{user_id}", response_model=ShowUserSchema, dependencies=[Depends(RoleChecker(acces_update_user))])
def update_user(user_id: int, updateUser: UpdateUserSchema, db: Session = Depends(db_connection)):
    userService = UserService(updateUser, db=db)
    return userService.update_item(user_id)


@userApi.delete("/delete", dependencies=[Depends(RoleChecker(acces_delete_user))])
def delete_user(user_id: int, db: Session = Depends(db_connection)):
    userService = UserService(db=db)
    return userService.delete_item(user_id)
