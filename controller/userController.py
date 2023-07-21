from controller.baseCrud import BaseCrud
from db.user_db import User as User
from schemas.schemas import UpdateUser as UpdateUserSchema


class UserController(BaseCrud):
        model = User
        updateSchema= None
        def __init__(self, updateSchema=None):
            self.updateSchema = updateSchema
            
        # def __init__(self):
        #     self.updateSchema = None
            
        # updateSchema = UpdateUserSchema