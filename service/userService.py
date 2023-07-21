from controller.userController import UserController
from service.baseService import BaseService


class UserService(BaseService):
    modelCtr = UserController
    updateSchema = None

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema
