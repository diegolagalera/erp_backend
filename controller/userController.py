from controller.baseCrud import BaseCrud
from db.models.user import User as User


class UserController(BaseCrud):
    model = User
    updateSchema = None

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema

    def user_exist(self, username: str):

        try:
            print('ooooooooooooooooo')
            # data_filter = {
            #     "username": "diegoooo",
            #     'limit': 2
            # }
            data_filter =[
                # {"username": "diego",'type': 'like'},
                # {"telefono": ['64440467', '64440469'],'type': 'in'},
                {"limit": "1"},
                {"offset": "0"}
                ]
            user, limit, offset = super().filter_and_paginate(data_filter)
            # print(**user)
            # print(user.items())
            for us in user:
                print(us.username)
            # print(user)
            return user
            #
            # print(total)
            # if not user:
            #     print('ppppppppppppp')
            #     print(user)
            #     return {"error no existe el usuario"}
        except:
            return

        # return user
