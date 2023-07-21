from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.UserSchemas import UserSchema
from typing import List


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



