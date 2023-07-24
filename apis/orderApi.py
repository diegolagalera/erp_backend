from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.UserSchemas import filter, UserSchema, ShowUserSchema, UpdateUserSchema, ShowUserSchemaPaginate, filterUserParamsSchema
from schemas.OrderSchemas import OrderSchema, ShowOrderSchema
from service.orderService import OrderService
from config.roleChecker import RoleChecker
from config.roleConstant import ROLES
from db.models.user import User
from apis.basic_user_auth import current_user
# from starlette.requests import Request


orderApi = APIRouter(
    prefix='/order', tags=["order"], responses={404: {"message": "NO FOUND ROUTA /user"}})

acces_get_ussers = [ROLES['ADMIN'], ROLES['USER']]
acces_get_usser = [ROLES['ADMIN'], ROLES['USER']]
acces_create_user = [ROLES['ADMIN']]
acces_update_user = [ROLES['ADMIN'], ROLES['USER']]
acces_delete_user = [ROLES['ADMIN'], ]


# @userApi.post("/", response_model=ShowUserSchemaPaginate, dependencies=[Depends(RoleChecker(acces_get_ussers))])
@orderApi.post("/", response_model=ShowUserSchemaPaginate)
def get_orders(filter_paginate: filter = None):
    userService = OrderService()
    # quita todos los valores NONES del filtro
    filter = filter_paginate.dict(exclude_unset=True)
    items, limit, offset = userService.get_items(filter['params'])
    response = ShowUserSchemaPaginate()
    response.items = items
    response.limit = limit
    response.offset = offset
    return response


@orderApi.get("/{user_id}", response_model=ShowUserSchema)
def get_order(user_id: int):
    userService = OrderService()
    return userService.get_item(user_id)


@orderApi.post("/create", response_model=OrderSchema, status_code=status.HTTP_201_CREATED )
async def create_order(order: OrderSchema,auth_user: ShowOrderSchema = Depends(current_user)):
    orderService = OrderService()
    # auth_user(request)
    if orderService.create_item(order,auth_user):
        return order
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario"
        )


@orderApi.patch("/{user_id}", response_model=ShowUserSchema)
def update_order(user_id: int, updateUser: UpdateUserSchema):
    userService = OrderService(updateUser)
    return userService.update_item(user_id)


@orderApi.delete("/delete")
def delete_order(user_id: int):
    userService = OrderService()
    return userService.delete_item(user_id)
