from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.UserSchemas import UserSchema, ShowUserSchema, UpdateUserSchema
from service.userService import UserService


userApi = APIRouter(
    prefix='/user', tags=["user"], responses={404: {"message": "NO FOUND ROUTA /user"}})


@userApi.get("/", response_model=List[ShowUserSchema])
def get_users():
    userService = UserService()
    return userService.get_items()


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
