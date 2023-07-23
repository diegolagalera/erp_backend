from controller.userController import UserController
from service.baseService import BaseService
from schemas.UserSchemas import UpdateUserSchema

from config.utils import get_hashed_password

class UserService(BaseService):
    modelCtr = UserController
    updateSchema = UpdateUserSchema

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema

    def create_item(self, item):
        try:
            print('hola')
            userCtr= UserController()
            return userCtr.user_exist(item.username)
            # if self.modelCtr.user_exist(item.username):
            #     pass
        except:
            pass

        # item.password = get_hashed_password(item.password)
        # return super().create_item(item)
        pass
