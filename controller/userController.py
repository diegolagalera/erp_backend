from controller.baseController import BaseController
from db.models.user import User as User
# from sqlalchemy.orm import Session
from config.database import db_connection
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from service.roleService import RoleService

from fastapi.encoders import jsonable_encoder


class UserController(BaseController):
    model = User
    updateSchema = None
    db = None

    def __init__(self, updateSchema=None, db=None):
        self.updateSchema = updateSchema
        self.db = db

    def user_exist(self, username: str, email: str):

        try:
            db= self.db
            user = db.query(self.model).filter(
                or_(self.model.username == username, self.model.email == email)).first()
            return user
        except:
            raise

    def order_user(self, user_id):
        db = db_connection
        db = next(db())
        item = db.query(self.model).filter(
            self.model.id == user_id).first()
        return item

    def update_item(self, item_id, role_list):
        db= self.db
        item = db.query(self.model).get(item_id)
        if not item:
            return {"msg": "elemento no encontrado"}
        item_update = self.updateSchema.dict(exclude_unset=True)
        # tenemos que elimanr los atributos que estan en modelo para actualizar
        if role_list:
            item_update.pop('roles')
        if 'addresses' in item_update:
            item_update.pop('addresses')
        # actualizamos con los nuevos datos el usuario

        for key, value in item_update.items():
            setattr(item, key, value)

        # actulizamos los roles del usuario
        if role_list != None:
            if len(role_list) != 0:
                create_role = []
                delete_role = []
                for rol in role_list:  # [1.2]
                    ids = []
                    for rol_actual in item.roles:  # [2,4]
                        ids.append(rol_actual.id)
                    if rol.id not in ids:
                        create_role.append(rol)
                for rol in item.roles:  # [2]
                    ids = []
                    for rol_actual in role_list:  # [1.2]
                        ids.append(rol_actual.id)
                    if rol.id not in ids:
                        delete_role.append(rol)
                # eliminamos los roles que no necesitamos
                for role_delete in delete_role:
                    item.roles.remove(role_delete)
                # agregamos los roles nuevos
                item.roles.extend(create_role)
            else:
                item.roles = []
        db.commit()
        user = db.query(self.model).get(item_id)
        return user

    def delete_item(self, item_id):
        db= self.db
        user = db.query(self.model).get(item_id)
        user.roles.clear()
        db.delete(user)
        db.commit()
        return {"msg": "elemento eliminado correctamente"}

        # return super().delete_item(item_id)
