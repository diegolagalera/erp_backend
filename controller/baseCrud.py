
from sqlalchemy import or_, DATETIME
import sqlalchemy
from sqlalchemy import cast
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config.database import db_connection
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import Query
# from fastapi_pagination import Page, paginate, add_pagination
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
disable_installed_extensions_check()
# from sqlalchemy.sql.expression import cast
from datetime import datetime
SQLALCHEMY_DATABSE_URL = os.getenv("DATA_BASE_URL")
engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class UserOut(BaseModel):
    username: str

    class Config:
        orm_mode = True


class BaseCrud():
    # MODELO DE LA TABLA EN BASE DE DATOS
    model = None
    # ESQUEMA QUE ACTUALIZARA SOLO LOS DATOS QUE SE ENVIEN
    updateSchema = None

    def __init__(self):
        # self.updateSchema = updateSchema
        pass

    def get_items(self, filter=None):
        """
        ENTRADA: 
        FILTER= [
            {"username": "diego",'type': 'like'},
            {"username": "diego",'type': '=='},
            {"telefono": ['64440467', '64440469'],'type': 'in'},
            {"apellido": '','type': '!='},
            {"limit": "2"},
            {"offset": "0"}
            ]
        SALIDA:
        ITEMS, LIMIT, OFFSET
        """
        return self.filter_and_paginate(filter)

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

    def filter_and_paginate(self, json_data=None):
        """
        EJEMPLO DE ENTRADA:
        json_data= [
            {"username": "diego",'type': 'like'},
            {"username": "diego",'type': '=='},
            {"telefono": ['64440467', '64440469'],'type': 'in'},
            {"apellido": '','type': '!='},
            {"creacion": [10/12/1997,10/12/1997] ,
            {"limit": "2"},
            {"offset": "0"}
            ]
        SALIDA:
            ITEMS, LIMIT, OFFSET
        """
        db: Session = db_connection
        db = next(db())
        query = db.query(self.model)
        limit = None
        offset = None
        # SI TENEMOS DATOS FILTRAREMOS Y EN CASO DE PAGINAR PAGINAMOS
        if json_data:
            search = [obj for obj in json_data if "text" in obj]
            # en caso que nos llegue el {'text' : 'busqueda libre'} buscaremos esa coinsidencia en todas las columnas
            if search:
                text = search[0]['text']
                filtros = []
                for column in self.model.__table__.columns:
                    filtros.append(
                        cast(column, sqlalchemy.String).like(f"%{text}%"))
                query = query.filter(or_(*filtros))
            # en caso contrario buscaremos por la columna especificada con el filtro especificado (==, like, !=, in)
            else:
                print('encontraddooooo')
                for obj in json_data:
                    keys = list(obj.keys())
                    column = getattr(self.model, keys[0], None)
                    if column is not None:
                        if column.type.python_type is datetime:
                            print('es una dataaaaaaaaa')
                            start_date=None
                            end_date = None
                            if len(obj[keys[0]]) == 1:
                                start_date = obj[keys[0]][0]
                            elif len(obj[keys[0]]) == 2:
                                start_date, end_date = obj[keys[0]]
                            
                            if start_date and end_date:
                                query = query.filter(column.between(start_date, end_date))
                                print('tengo las dos data')
                            elif start_date:
                                query = query.filter(column >= start_date)
                                print('solo startt')
                            elif end_date:
                                query = query.filter(column <= end_date)
                                print('solo finallll')
                            raise HTTPException(
                                        status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f"el formato del filtro de data es incorrecto se requiere [date_start, date_end] o [null, date_end] o [date]"
                                    )
                        elif 'type' in obj:
                            if obj['type'] == '==':
                                query = query.filter(column == obj[keys[0]])
                            elif obj['type'] == 'like':
                                print('likeeeeeeeeeeeeeeee')
                                query = query.filter(
                                    cast(column, sqlalchemy.String).like(f"%{str(obj[keys[0]])}%"))
                            elif obj['type'] == '!=':
                                query = query.filter(column != obj[keys[0]])
                            elif obj['type'] == 'in':
                                print('tontooooooo')
                                typeobj = obj[keys[0]]
                                print(type(typeobj))
                                if isinstance(typeobj, list):
                                    print('es una listaaa')
                                    query = query.filter(
                                        column.in_(obj[keys[0]]))
                                else:
                                    raise HTTPException(
                                        status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f"para hacer un in tiene que pasar una lista no un string "
                                    )

                            else:  # si el segundo parametro del objeto
                                raise HTTPException(
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"error con el type del filtro '{column}'"
                                )
                        else:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="tiene que especificar el parametro type con algun valor (==, like, !=, in) ex: {'username':'pepe', 'type':'like}'"
                            )
                    elif "limit" in obj:
                        limit = int(obj["limit"])
                    elif "offset" in obj:
                        offset = int(obj["offset"])
                # PAGINACION SOLO SI TENEMOS LIMIT Y OFFSET EN CASO CONTRARIO RETORNAMOS TDOS LOS ELEMENTOS
                print('forraaa')
                # print(limit)
                # print(query)
                # if limit and (offset or offset == 0):
                #     print('paginate')
                #     try:
                #         items = query.offset(
                #             offset).limit(limit).all()
                #     except:
                #         pass
                # else:
                #     items = query.all()
            
            limit_obj = [obj for obj in json_data if "limit" in obj]
            offset_obj = [obj for obj in json_data if "offset" in obj]
            print(limit_obj)
            print(offset_obj)
            if limit_obj and offset_obj:
                limit = limit_obj[0]['limit']
                print('kkkkkklllllll')
                offset = offset_obj[0]['offset']
                print('paginate')
                print(query)
                try:
                    items = query.offset(
                        offset).limit(limit).all()
                except:
                    pass
            else:
                items = query.all()
        else:
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkk')
            print(query)
            items = query.all()
        return items, limit, offset
        # return {items:items, limit:limit, offset:offset}
