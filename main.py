from fastapi import FastAPI
from typing import Union
from fastapi.staticfiles import StaticFiles
import logging
from config.log_config import init_loggers
init_loggers()
log = logging.getLogger("app")
app = FastAPI()


def load_env_var():
    log.info('CARGANDO VARIABLE DE ENTORNO .ENV')
    from dotenv import find_dotenv, load_dotenv
    datoenv_path = find_dotenv()
    load_dotenv(datoenv_path)


def create_tables():
    log.info('CREANDO TABLAS EN BASE DE DATOS')
    # from config.database import Base, engine
    from config.database import engine
    from db.models.base import Base
    from sqlalchemy import event
    from db.datos.datos import create_data
    from config.roleConstant import defineRoleConstant
    Base.metadata.create_all(bind=engine)
    # TODO ELIMINAR ESTA SECCION DE CREAR DATOS DE PRUEBA A LA BASE DE DATOS
    create_data()
    defineRoleConstant()


def load_sub_apis():
    log.info('CARGANDO TODAS LAS RUTAS API DE LOS DIRECTORIOS')
    from apis.gneral import General
    from apis import basic_user_auth, userApi
    app.include_router(General.general)
    app.include_router(basic_user_auth.auth)
    app.include_router(userApi.userApi)
    app.mount("/static", StaticFiles(directory="static"), name="static")


load_env_var()
create_tables()
load_sub_apis()
