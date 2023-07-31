from controller.userController import UserController
from service.baseService import BaseService
from db.models.user import UpdateUserSchema
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from db.models.user import User
from config.database import db_connection

from config.utils import get_hashed_password
from service.roleService import RoleService


class UserService(BaseService):
    modelCtr = UserController
    updateSchema = UpdateUserSchema

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema

    def create_item(self, item):
        try:
            user_ctr = UserController()
            userExist = user_ctr.user_exist(item.username, item.email)
            if not userExist:
                item = item.dict()
                roles = item.pop('roles')
                user = User(**item)
                user.password = get_hashed_password(user.password)
                if roles:
                    for rol in roles:
                        role = RoleService().get_item(rol)
                        if role:
                            user.roles.append(role)

                return user_ctr.create_item(user, is_model=True)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya existe"
                )
        except SQLAlchemyError as e:  # captura algun error que se propague de la base de datos
            raise e

    def update_item(self, user_id: int):
        itemToUpdate = self.updateSchema.dict()
        roles = itemToUpdate['roles']
        user_ctr = UserController(self.updateSchema)
        role_list = []
        if roles:
            role_list = []
            for rol in roles:
                role_list.append(RoleService().get_item(rol))
        if roles == None:
            return user_ctr.update_item(user_id, None)
        else:
            return user_ctr.update_item(user_id, role_list)

    def delete_item(self, item_id: int):
        user_ctr = UserController()
        return user_ctr.delete_item(item_id)
        # return super().delete_item(item_id)
