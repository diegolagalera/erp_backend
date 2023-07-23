from fastapi import FastAPI
from typing import Union
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate

app = FastAPI()
add_pagination(app)
# CARGAMOS TODAS LAS VARIABLE DEL .ENV
def load_env_var():
    from dotenv import find_dotenv, load_dotenv
    datoenv_path = find_dotenv()
    load_dotenv(datoenv_path)

# CARGAMOS LOS MODELOS A LA BASE DE DATOS
def create_tables():
    from config.database import Base, engine
    Base.metadata.create_all(bind=engine)
   

# CARGAMOS LAS SUB APIS DE LOS MODELOS
def load_sub_apis():
    from apis.gneral import General
    from apis import basic_user_auth, userApi
    # -------------------------------------------------------------------------- #
    app.include_router(General.general)
    app.include_router(basic_user_auth.auth)
    app.include_router(userApi.userApi)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    # -------------------------------------------------------------------------- #

load_env_var()
load_sub_apis()
create_tables()
