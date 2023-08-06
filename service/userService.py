from controller.userController import UserController
from service.baseService import BaseService
from db.models.user import UpdateUserSchema
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from db.models.user import User
from db.models.address import Address, UpdateAddressSchema
from service.addressService import AddressService
from config.database import db_connection

from config.utils import get_hashed_password
from service.roleService import RoleService


class UserService(BaseService):
    modelCtr = UserController
    updateSchema = UpdateUserSchema
    db = None

    def __init__(self, updateSchema=None, db=None):
        self.updateSchema = updateSchema
        self.db = db

    def create_item(self, item):
        try:
            user_ctr = UserController(db=self.db)
            userExist = user_ctr.user_exist(item.username, item.email)
            if not userExist:
                # CREAMOS LOS USUARIOS, ASIGNAMOS LOS ROLES
                item = item.dict()
                roles = item.pop('roles')
                addresses = item.pop('addresses')
                user = User(**item)
                user.password = get_hashed_password(user.password)
                if roles:
                    for rol in roles:
                        role = RoleService(db=self.db).get_item(rol)
                        if role:
                            user.roles.append(role)
                userResponse = user_ctr.create_item(user, is_model=True)

                #  SI EL USUARIO ESTA CREADO CREAMOS Y LE ASIGNAMOS LA DIRECCION
                if userResponse.id:
                    if addresses:
                        addresses['user_id'] = userResponse.id
                        addressService = AddressService(db=self.db)
                        addressService.create_item(addresses)
                        # self.db.flush()

                # NOTA: al ser una transaccion el commit() lo hace automaticamente el ultimo create_item()sin enviar el transaction=true
                # mientras tanto puedo ejecutar todos los create_item(xxx, transction=true) que en caso de error se hace un rollback de todo
                # self.db.commit()
                return userResponse
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya existe"
                )
        except SQLAlchemyError as e:  # captura algun error que se propague de la base de datos
            self.db.rollback()
            raise e
        except:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail="Error al crear el usuario y la dirección.")

    def update_item(self, user_id: int):
        itemToUpdate = self.updateSchema.dict()
        roles = itemToUpdate['roles']
        addresses = itemToUpdate['addresses']
        user_ctr = UserController(self.updateSchema, db=self.db)
        role_list = None
        if roles:
            role_list = []
            for rol in roles:
                role_list.append(RoleService(db=self.db).get_item(rol))
        if addresses:
            addressService = AddressService(db=self.db)
            addressService.update_items(addresses)
            # print('addreesssssss')
            # print(addresses)
            # for address in addresses:
            #     print(address)
            #     updateAddress = UpdateAddressSchema(address)
            #     print(updateAddress)
            #     print(updateAddress.street)
            #     AddressService(db=self.db, updateSchema=updateAddress)
            # updateAddress = AddressService.update_item(itemToUpdate['roles'])
        # if roles == None:
        #     return user_ctr.update_item(user_id, None)
        # else:
        return user_ctr.update_item(user_id, role_list)

    def delete_item(self, item_id: int):
        user_ctr = UserController()
        return user_ctr.delete_item(item_id)
        # return super().delete_item(item_id)
