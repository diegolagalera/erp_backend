from controller.baseController import BaseController
from db.models.role import Role
# from sqlalchemy.orm import Session
from config.database import db_connection
from sqlalchemy import or_
from schemas.OrderSchemas import ShowOrderSchema, UpdateOrderSchema


class RoleController(BaseController):
    model = Role
    updateSchema = None
    db = None

    def __init__(self, updateSchema=None, db=None):
        self.updateSchema = updateSchema
        self.db = db
