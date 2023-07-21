from controller.baseCrud import BaseCrud
from db.user_db import User as User


class UserController(BaseCrud):
    model = User
    updateSchema = None

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema
