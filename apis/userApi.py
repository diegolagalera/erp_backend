from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from db.models.user import filter, UserSchema, ShowUserSchema, UpdateUserSchema, ShowUserSchemaPaginate, filterUserParamsSchema
from service.userService import UserService
from config.roleChecker import RoleChecker
from config.roleConstant import ROLES
from fastapi.encoders import jsonable_encoder
from dateutil.parser import parse as parse_datetime
from config.database import db_connection

userApi = APIRouter(
    prefix='/user', tags=["user"], responses={404: {"message": "NO FOUND ROUTA /user"}})

acces_get_ussers = [ROLES['admin'], ROLES['user']]
acces_get_usser = [ROLES['admin'], ROLES['user']]
acces_create_user = [ROLES['admin']]
acces_update_user = [ROLES['admin'], ROLES['user']]
acces_delete_user = [ROLES['admin'], ]

# @userApi.post("/", response_model=ShowUserSchemaPaginate)

@userApi.post("/", response_model=ShowUserSchemaPaginate, dependencies=[Depends(RoleChecker(acces_get_ussers))])
def get_users(filter_paginate: filter = None):
    print(jsonable_encoder(filter_paginate))
    userService = UserService()
    # quita todos los valores NONES del filtro
    filter = filter_paginate.dict(exclude_unset=True)
    items, limit, offset = userService.get_items(filter['params'])
    response = ShowUserSchemaPaginate()
    response.items = items
    response.limit = limit
    response.offset = offset
    return response


@userApi.get("/{user_id}", response_model=ShowUserSchema)
def get_user(user_id: int):
    userService = UserService()
    response= userService.get_item(user_id)
    print('hhhhhhhh')
    print(jsonable_encoder(response))
    print(jsonable_encoder(response.roles))
    return response


@userApi.post("/create", response_model=ShowUserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    userService = UserService()
    return userService.create_item(user)


@userApi.patch("/{user_id}", response_model=ShowUserSchema)
def update_user(user_id: int, updateUser: UpdateUserSchema):
    userService = UserService(updateUser)
    response =userService.update_item(user_id)

    print(jsonable_encoder(response))
    return response

@userApi.delete("/delete")
def delete_user(user_id: int):
    userService = UserService()
    return userService.delete_item(user_id)
