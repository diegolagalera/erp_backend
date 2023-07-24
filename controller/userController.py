from controller.baseController import BaseController
from db.models.user import User as User
from sqlalchemy.orm import Session
from config.database import db_connection
from sqlalchemy import or_


class UserController(BaseController):
    model = User
    updateSchema = None

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema

    def user_exist(self, username: str, email: str):

        try:
            db: Session = db_connection
            db = next(db())
            user = db.query(self.model).filter(or_(self.model.username == username,self.model.email ==email )).first()
            return user
        except:
            raise
