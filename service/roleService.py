from controller.roleController import RoleController
from service.baseService import BaseService
from db.models.role import UpdateRoleSchema
# from fastapi import HTTPException, status
# from fastapi.encoders import jsonable_encoder
import logging
log = logging.getLogger("app")


class RoleService(BaseService):
    modelCtr = RoleController
    updateSchema = UpdateRoleSchema
    db = None

    def __init__(self, updateSchema=None, db=None):
        self.updateSchema = updateSchema
        self.db = db
