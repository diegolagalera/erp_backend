from fastapi import FastAPI
from typing import Union
# IMPORTAR VARIABLES DE ENTORNO .ENV
from dotenv import find_dotenv, load_dotenv
datoenv_path =find_dotenv()
load_dotenv(datoenv_path)

from fastapi.staticfiles import StaticFiles
from apis.gneral import General
from apis.user import basic_user_auth, userApi
from config.database import Base, engine



app = FastAPI()
# Routers
app.include_router(General.general)
app.include_router(basic_user_auth.auth)
app.include_router(userApi.userApi)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



def create_tables():
    Base.metadata.create_all(bind=engine)
    
create_tables()