from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging
from config.log_config import init_loggers
init_loggers()
log = logging.getLogger("app")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://localhost:3001",

]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    from db.datos.datos import create_data
    from config.roleConstant import defineRoleConstant
    Base.metadata.create_all(bind=engine)
    # TODO ELIMINAR ESTA SECCION DE CREAR DATOS DE PRUEBA A LA BASE DE DATOS
    # create_data()
    defineRoleConstant()


def load_sub_apis():
    log.info('CARGANDO TODAS LAS RUTAS API DE LOS DIRECTORIOS')
    from apis.gneral import General
    from apis import basic_user_auth, userApi, orderApi, roleApi
    app.include_router(General.general)
    app.include_router(basic_user_auth.auth)
    app.include_router(userApi.userApi)
    app.include_router(orderApi.orderApi)
    app.include_router(roleApi.roleApi)
    app.mount("/static", StaticFiles(directory="static"), name="static")


load_env_var()
create_tables()
load_sub_apis()
