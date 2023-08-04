from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
# from schemas.UserSchemas import ShowUserSchema, UpdateUserSchema
from db.models.user import ShowUserSchema, UpdateUserSchema
from schemas.OrderSchemas import OrderSchema, ShowOrderSchema, ShowOrderSchemaPaginate, filter, UpdateOrderSchema
from service.orderService import OrderService
from config.roleChecker import RoleChecker
from config.roleConstant import ROLES
from db.models.user import User
from apis.basic_user_auth import current_user
# from starlette.requests import Request
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from fastapi.encoders import jsonable_encoder

orderApi = APIRouter(
    prefix='/order', tags=["order"], responses={404: {"message": "NO FOUND ROUTA /user"}})

acces_get_ussers = [ROLES['admin'], ROLES['user']]
acces_get_usser = [ROLES['admin'], ROLES['user']]
acces_create_user = [ROLES['admin']]
acces_update_user = [ROLES['admin'], ROLES['user']]
acces_delete_user = [ROLES['admin'], ]


# @userApi.post("/", response_model=ShowUserSchemaPaginate, dependencies=[Depends(RoleChecker(acces_get_ussers))])
@orderApi.post("/", response_model=ShowOrderSchemaPaginate)
def get_orders(filter_paginate: filter = None):
    orderService = OrderService()
    # quita todos los valores NONES del filtro
    filter = filter_paginate.dict(exclude_unset=True)
    items, limit, offset = orderService.get_items(filter['params'])
    response = ShowOrderSchemaPaginate()
    response.items = items
    response.limit = limit
    response.offset = offset
    return response


@orderApi.get("/{order_id}", response_model=ShowOrderSchema)
async def get_order(order_id: int):
    orderService = OrderService()
    return orderService.get_item(order_id)


@orderApi.post("/create", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderSchema, auth_user: ShowUserSchema = Depends(current_user)):
    orderService = OrderService()
    # auth_user(request)
    if orderService.create_item(order, auth_user):
        return order
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario"
        )


@orderApi.patch("/{order_id}", response_model=ShowOrderSchema)
def update_order(order_id: int, updateUser: UpdateOrderSchema):
    orderService = OrderService(updateUser)
    return orderService.update_item(order_id)


@orderApi.delete("/delete")
def delete_order(order_id: int):
    userService = OrderService()
    return userService.delete_item(order_id)

@orderApi.get("/user/orders")
async def order_user(user_id:Optional[int]=None,auth_user: ShowUserSchema = Depends(current_user, use_cache=True)):
    userService = OrderService()
    if user_id:
        user = userService.order_user(user_id)
    else:
        user = response = userService.order_user(auth_user.id)
    response = jsonable_encoder(user)
    response['orders'] = jsonable_encoder(user.orders)

    return "holaa"

# async def order_user(user_id:Optional[int]=None):
