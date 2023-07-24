from controller.orderController import OrderController
from service.baseService import BaseService
from schemas.OrderSchemas import ShowOrderSchema,UpdateOrderSchema
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from service.userService import UserService
# from fastapi.encoders import jsonable_encoder
import logging
log = logging.getLogger("app")


class OrderService(BaseService):
    modelCtr = OrderController
    updateSchema = UpdateOrderSchema

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema

    def create_item(self, item,auth_user):
        log.info('Create item order')
        print(auth_user.id)
        orderCtr = OrderController()
        userService = UserService()

        if item.user_id:
            user:ShowOrderSchema= userService.get_item(item.user_id)
            return orderCtr.create_item(item,user)

            print('guaradar con este usuario')
        else:
            print('dentroooooooo')
            if (auth_user):
                user:ShowOrderSchema= userService.get_item(auth_user.id)
                return orderCtr.create_item(item,user)
                # print(jsonable_encoder(auth))
            else:
                print('error al obtener usuario authenticado')
        return "error"
    # def create_item(self, item):
    #     try:
    #         orderCtr = OrderController()
    #         user = orderCtr.user_exist(item.username, item.email)
    #         if not user:
    #             item.password = get_hashed_password(item.password)
    #             return super().create_item(item)
    #         else:
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 detail="El usuario ya existe"
    #             )
    #     except SQLAlchemyError as e:  # captura algun error que se propague de la base de datos
    #         raise e
