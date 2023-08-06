from controller.addressController import AddressController
from service.baseService import BaseService
from db.models.address import UpdateAddressSchema
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from db.models.user import User
from config.database import db_connection

from config.utils import get_hashed_password
from service.roleService import RoleService


class AddressService(BaseService):
    modelCtr = AddressController
    updateSchema = UpdateAddressSchema
    db = None

    def __init__(self, updateSchema=None, db=None):
        self.updateSchema = updateSchema
        self.db = db

    def update_items(self, addresses: list):
        print('addreesssssss')
        # print(addresses['street'])
        for address in addresses:
            # address = address.d
            print(address['street'])
            updateAddress = UpdateAddressSchema(
                id=address['id'],
                street=address['street'],
                province=address['province'],
                city=address['city'],
                postal_code=address['postal_code'],
                others=address['others']
            )
            self.updateSchema = updateAddress
            super().update_item(address['id'])
            print(',,,,,,,,,,,,,,,,,,,,,,,,,')
            print(updateAddress)
            print(updateAddress.street)
        return
