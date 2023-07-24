from controller.userController import UserController
from service.baseService import BaseService
from schemas.UserSchemas import UpdateUserSchema
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from config.utils import get_hashed_password


class UserService(BaseService):
    modelCtr = UserController
    updateSchema = UpdateUserSchema

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema

    def create_item(self, item):
        try:
            userCtr = UserController()
            user = userCtr.user_exist(item.username, item.email)
            if not user:
                item.password = get_hashed_password(item.password)
                return super().create_item(item)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya existe"
                )
        except SQLAlchemyError as e:  # captura algun error que se propague de la base de datos
            raise e
