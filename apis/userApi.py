from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.UserSchemas import filter, UserSchema, ShowUserSchema, UpdateUserSchema, ShowUserSchemaPaginate, filterUserParamsSchema
from service.userService import UserService
from config.roleChecker import RoleChecker
from config.roleConstant import ROLES
userApi = APIRouter(
    prefix='/user', tags=["user"], responses={404: {"message": "NO FOUND ROUTA /user"}})

@userApi.post("/", response_model=ShowUserSchemaPaginate, dependencies=[Depends(RoleChecker([ROLES['USER'],ROLES['ADMIN']]))])
def get_users(filter_paginate: filter = None):
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
    return userService.get_item(user_id)


@userApi.post("/create", response_model=ShowUserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    userService = UserService()
    if userService.create_item(user):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario"
        )


@userApi.patch("/{user_id}", response_model=ShowUserSchema)
def update_user(user_id: int, updateUser: UpdateUserSchema):
    userService = UserService(updateUser)
    return userService.update_item(user_id)


@userApi.delete("/delete")
def delete_user(user_id: int):
    userService = UserService()
    return userService.delete_item(user_id)
