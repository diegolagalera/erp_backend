from fastapi import APIRouter
from typing import Union
general = APIRouter(prefix='/general', tags=["general"], responses={404 : {"message": "NO FOUND ROUTA /general"}})


# @general.get("/hi")
# def read_subroot():
#     return {"Hello": "World"}


# @general.get("/itemss/{item_id}")
# def read_subitem(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


