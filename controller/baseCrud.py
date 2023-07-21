
from sqlalchemy.orm import Session
from config.database import user_connection
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
SQLALCHEMY_DATABSE_URL = os.getenv("DATA_BASE_URL")
engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal= sessionmaker(bind=engine, autocommit=False, autoflush=False)
class BaseCrud():
    model=None
    updateSchema= None
    def __init__(self):
        # self.updateSchema = updateSchema
        pass

    def get_item(self, item_id):
        db: Session = user_connection
        db= next(db())
        item = db.query(self.model).filter(self.model.id == item_id).first()
        if not item:
            return {"msg": "item no encontrado"}
        return item

    def get_list(self):
        db: Session = user_connection
        db= next(db())
        users = db.query(self.model).all()
        return users


    def create(self, item):
        db: Session = user_connection
        db= next(db())
        newItem = self.model(**item)
        db.add(newItem)
        db.commit()
        db.refresh(newItem)
        return "todo ok en el usuario"


    def update(self, item_id):
        db: Session = user_connection
        db= next(db())
        item = db.query(self.model).filter(self.model.id == item_id)
        if not item.first():
            return {"msg": "usuario no encontrado"}
        item.update(self.updateSchema.dict(exclude_unset=True))
        db.commit()
        return {"msg": "usuario actualizado correctamente"}


    def delete(self, item_id):
        db: Session = user_connection
        db= next(db())
        item = db.query(self.model).filter(self.model.id == item_id)

        if not item.first():
            return {"msg": "usuario no encontrado"}
        item.delete(synchronize_session=False)
        db.commit()
        return {"msg": "usuario eliminado correctamente"}
        
    