from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from schemas.schemas import showUser as showUserSchema
from schemas.schemas import User as UserSchema
from service.userService import UserService
from schemas.schemas import UpdateUser as UpdateUserSchema

userApi = APIRouter(
    prefix='/user', tags=["user"], responses={404: {"message": "NO FOUND ROUTA /user"}})

@userApi.get("/", response_model=List[showUserSchema])
def get_users():
    userService = UserService()
    return userService.get_users()


@userApi.post("/create")
def create_user(user: UserSchema):
    userService = UserService()
    return userService.create_user(user)
   


@userApi.get("/{user_id}", response_model=showUserSchema)
def get_user(user_id: int):
    userService = UserService()
    return userService.get_user(user_id)
   


@userApi.delete("/delete")
def delete_user(user_id: int):
    userService = UserService()
    return userService.delete_user(user_id)
   


@userApi.patch("/{user_id}")
def update_user(user_id: int, updateUser:UpdateUserSchema):
    userService = UserService()
    return userService.update_user(user_id,updateUser)