from controller.userController import UserController
from schemas.schemas import User as UserSchema
from schemas.schemas import UpdateUser as UpdateUserSchema


class UserService():
    def get_users(self):
        userCtr = UserController()
        return userCtr.get_list()


    def create_user(self,user: UserSchema):
        userCtr = UserController()
        response = userCtr.create(user.dict())
        return response
    


    def get_user(self,user_id: int):
        userCtr = UserController()
        return userCtr.get_item(user_id)
    


    def delete_user(self,user_id: int):
        userCtr = UserController()
        return userCtr.delete(user_id)
    


    def update_user(self,user_id: int, updateUser:UpdateUserSchema):
        print('ppppppppppppppppppp')
        userCtr = UserController(updateUser)
        return userCtr.update(user_id)