from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
# from schemas.UserSchemas import ShowUserSchema, UpdateUserSchema
# from schemas.OrderSchemas import OrderSchema, ShowOrderSchema, ShowOrderSchemaPaginate, filter, UpdateOrderSchema
# from service.orderService import OrderService
from service.roleService import RoleService
from db.models.role import ShowRoleSchemaPaginate, ShowRoleSchema, filter, RoleSchema, UpdateRoleSchema
from config.roleChecker import RoleChecker
from config.roleConstant import ROLES
# from db.models.user import User
from apis.basic_user_auth import current_user
# from starlette.requests import Request
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from fastapi.encoders import jsonable_encoder
from config.database import db_connection
from sqlalchemy.orm import Session

roleApi = APIRouter(
    prefix='/role', tags=["role"], responses={404: {"message": "NO FOUND ROUTA /role"}})

acces_get_ussers = [ROLES['admin'], ROLES['user']]
acces_get_usser = [ROLES['admin'], ROLES['user']]
acces_create_user = [ROLES['admin']]
acces_update_user = [ROLES['admin'], ROLES['user']]
acces_delete_user = [ROLES['admin'], ]


# @userApi.post("/", response_model=ShowUserSchemaPaginate, dependencies=[Depends(RoleChecker(acces_get_ussers))])
@roleApi.post("/", response_model=ShowRoleSchemaPaginate)
def get_orders(filter_paginate: filter = None):
    roleService = RoleService()
    # quita todos los valores NONES del filtro
    filter = filter_paginate.dict(exclude_unset=True)
    items, limit, offset = roleService.get_items(filter['params'])
    response = ShowRoleSchemaPaginate()
    response.items = items
    response.limit = limit
    response.offset = offset
    return response


@roleApi.get("/{role_id}", response_model=ShowRoleSchema)
async def get_order(role_id: int, db: Session = Depends(db_connection)):
    print('gggg')
    print(db)
    roleService = RoleService(db=db)
    response = roleService.get_item(role_id)
    print(response.users)
    return response


@roleApi.post("/create", response_model=ShowRoleSchema, status_code=status.HTTP_201_CREATED)
async def create_order(order: RoleSchema):
    roleService = RoleService()
    # auth_user(request)
    try:
        return roleService.create_item(order)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario"
        )


@roleApi.patch("/{role_id}", response_model=ShowRoleSchema)
def update_order(role_id: int, updateRole: UpdateRoleSchema):
    roleService = RoleService(updateRole)
    return roleService.update_item(role_id)


@roleApi.delete("/delete")
def delete_order(role_id: int):
    roleService = RoleService()
    return roleService.delete_item(role_id)


# async def order_user(user_id:Optional[int]=None):
