from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.UserSchemas import UserSchema, ShowUserSchema
from fastapi.encoders import jsonable_encoder

# from sqlalchemy.orm import Session
from config.database import db_connection
from db.models.user import User
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette.requests import Request

import logging
log = logging.getLogger("app")
ALGORITM = "HS256"
ACCESS_TOKE_DURATION = 60
SECRET = 'e01a4f0700f6ef76c7b0820972dc472b08b15786c716b0cc688cae39b277a33c'
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth = APIRouter(
    prefix='/auth', tags=["auth"], responses={404: {"message": "NO FOUND ROUTA /user"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

# coge el token de oauth2, lo decodifica y coge el username
# def auth_user(token: str = Depends(oauth2),  db: Session = Depends(db_connection)):
def auth_user(token: str = Depends(oauth2),  db = Depends(db_connection)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=" usuario no encontrado",
        headers={"WWW-Authenticate": "Bearer"})

    exception_time_out = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="session expirada, no tiene accesso",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        print('kkkkkkkkkkkkkkk')
        username = jwt.decode(token, SECRET, algorithms=[ALGORITM]).get('sub')
        if username is None:
            raise exception
    except JWTError:
        raise exception_time_out

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise exception

    return user


def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"})
    return user


@auth.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db = Depends(db_connection)):
    try:
        user = db.query(User).filter(User.username == form.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no existe"
            )

        if not crypt.verify(form.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cotraseña incorrecta"
            )
        data = {
            "sub": user.username,
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKE_DURATION)
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al hacer login"
        )

    return {"access_token": jwt.encode(data, SECRET, algorithm=ALGORITM), "token_type": "bearer"}
    # print(jsonable_encoder(user))


@auth.get("/me", response_model=ShowUserSchema)
def me(user: UserSchema = Depends(current_user)):
    return user

# NO BORRAR ESTO SIRVE PARA VER VER SI UN USUARIO ESTA LOGEADO O NO SIN QUE RETORNE UN ERROR DE OAUTH2, AQUI PODREMOS CONTROLAR NOSOTROS EL ERROR
# def auth_user(request: Request):
#     print('kkkksdasd')
#     print(request.headers)
#     token = request.headers.get("Authorization")
#     print(token)
#     # print(oauth2(request))
#     # token = oauth2(request)
#     print('uuuuuuuuuuuuuuuuuuuuu')
#     # print(token)
#     username = jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJpZCI6MSwiZXhwIjoxNjkwMjE1NDQ0fQ.fUchwkN91v-eZruzLBHM14P5lraYfOSLOlvhPXlFW_0', SECRET, algorithms=[ALGORITM]).get('id')
#     print(str(username))
#     return