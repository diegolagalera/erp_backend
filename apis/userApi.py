from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.UserSchemas import filter, UserSchema, ShowUserSchema, UpdateUserSchema, ShowUserSchemaPaginate,filterUserParamsSchema
from service.userService import UserService
from fastapi_pagination import LimitOffsetPage, Page, add_pagination


userApi = APIRouter(
    prefix='/user', tags=["user"], responses={404: {"message": "NO FOUND ROUTA /user"}})

add_pagination(userApi)


@userApi.post("/", response_model=ShowUserSchemaPaginate)
def get_users(filter_paginate:filter=None):
    userService = UserService()
    print('filterrrr')
    t =filter_paginate.dict(exclude_unset=True)
    print(t['params'])
    # print(filter_paginate.dict())
    items, limit, offset = userService.get_items(t['params'])
    # print(items)
    response = ShowUserSchemaPaginate()
    response.items=items
    response.limit= limit
    response.offset=offset
    return response


@userApi.get("/{user_id}", response_model=ShowUserSchema)
def get_user(user_id: int):
    userService = UserService()
    return userService.get_item(user_id)


@userApi.post("/create")
def create_user(user: UserSchema):
    userService = UserService()
    return userService.create_item(user)


@userApi.patch("/{user_id}")
def update_user(user_id: int, updateUser: UpdateUserSchema):
    userService = UserService(updateUser)
    return userService.update_item(user_id)


@userApi.delete("/delete")
def delete_user(user_id: int):
    userService = UserService()
    return userService.delete_item(user_id)
