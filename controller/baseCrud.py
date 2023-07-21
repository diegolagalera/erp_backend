
from sqlalchemy.orm import Session
from config.database import db_connection
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
SQLALCHEMY_DATABSE_URL = os.getenv("DATA_BASE_URL")
engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class BaseCrud():
    # MODELO DE LA TABLA EN BASE DE DATOS
    model = None
    # ESQUEMA QUE ACTUALIZARA SOLO LOS DATOS QUE SE ENVIEN
    updateSchema = None

    def __init__(self):
        # self.updateSchema = updateSchema
        pass

    def get_items(self):
        db: Session = db_connection
        db = next(db())
        users = db.query(self.model).all()
        return users

    def get_item(self, item_id):
        db: Session = db_connection
        db = next(db())
        item = db.query(self.model).filter(self.model.id == item_id).first()
        if not item:
            return {"msg": "item no encontrado"}
        return item

    def create_item(self, item):
        db: Session = db_connection
        db = next(db())
        newItem = self.model(**item)
        db.add(newItem)
        db.commit()
        db.refresh(newItem)
        return "todo ok en el usuario"

    def update_item(self, item_id):
        db: Session = db_connection
        db = next(db())
        item = db.query(self.model).filter(self.model.id == item_id)
        if not item.first():
            return {"msg": "usuario no encontrado"}
        item.update(self.updateSchema.dict(exclude_unset=True))
        db.commit()
        return {"msg": "usuario actualizado correctamente"}

    def delete_item(self, item_id):
        db: Session = db_connection
        db = next(db())
        item = db.query(self.model).filter(self.model.id == item_id)

        if not item.first():
            return {"msg": "usuario no encontrado"}
        item.delete(synchronize_session=False)
        db.commit()
        return {"msg": "usuario eliminado correctamente"}
