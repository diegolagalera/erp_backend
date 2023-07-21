from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.database import user_connection
from sqlalchemy.orm import Session
from db.user_db import User as US
from schemas.schemas import User as UserSchema
from schemas.schemas import showUser as showUserSchema
from schemas.schemas import UpdateUser as UpdateUserSchema
from typing import List
from controller.baseCrud import BaseCrud

from controller.userController import UserController

auth = APIRouter(
    prefix='/auth', tags=["auth"], responses={404: {"message": "NO FOUND ROUTA /user"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# class User(BaseModel):
#     username : str
#     full_name: str
#     email: str
#     disabled: str


def current_user(toke: str = Depends(oauth2)):
    # TODO retorna el usuario
    user = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"})

    return {"ok"}


@auth.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    form.username
    form.password
    user = None
    # user =db.get()
    if not user:
        raise HTTPException(status_code=400, detail="el ususrio no existe")

    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña es incorrecta")

    return {"access_token": "testtoken", "token_type": "bearer"}


@auth.get("/me")
def me(user: UserSchema = Depends(current_user)):
    return {""}



