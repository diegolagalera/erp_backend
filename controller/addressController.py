from controller.baseController import BaseController
from db.models.address import Address
# from sqlalchemy.orm import Session
from config.database import db_connection
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from service.roleService import RoleService

from fastapi.encoders import jsonable_encoder


class AddressController(BaseController):
    model = Address
    updateSchema = None
    db = None

    def __init__(self, updateSchema=None, db=None):
        self.updateSchema = updateSchema
        self.db = db

   