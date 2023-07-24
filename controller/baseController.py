
from datetime import datetime
from sqlalchemy import or_, cast
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.database import db_connection
from fastapi import HTTPException, status
import logging
log = logging.getLogger("app")


class BaseController():
    # MODELO DE LA TABLA EN BASE DE DATOS
    model = None
    # ESQUEMA QUE ACTUALIZARA SOLO LOS DATOS QUE SE ENVIEN
    updateSchema = None

    def __init__(self):
        # self.updateSchema = updateSchema
        pass

    def get_items(self, filter=None):
        log.info(f'Get Items {self.__class__.__name__}')
        return self.filter_and_paginate(filter)

    def get_item(self, item_id):
        log.info(f'Get Item {self.__class__.__name__}')
        try:
            db: Session = db_connection
            db = next(db())
            item = db.query(self.model).filter(
                self.model.id == item_id).first()
            if not item:
                return {"msg": "item no encontrado"}
            return item
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al obtener elemento de la BD " + str(e)
            )

    def create_item(self, item):
        log.info(f'Create Item {self.__class__.__name__}')
        try:
            db: Session = db_connection
            db = next(db())
            newItem = self.model(**item)
            db.add(newItem)
            db.commit()
            db.refresh(newItem)
            return newItem
            # return "todo ok en el usuario"
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al insertar a la BD " + str(e)
            )

    def update_item(self, item_id):
        log.info(f'Update Item {self.__class__.__name__}')
        try:
            db: Session = db_connection
            db = next(db())
            item = db.query(self.model).filter(self.model.id == item_id)
            if not item.first():
                return {"msg": "usuario no encontrado"}
            item.update(self.updateSchema.dict(exclude_unset=True))
            db.commit()
            return db.query(self.model).filter(self.model.id == item_id).first()

            # return {"msg": "usuario actualizado correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar a la BD " + str(e)
            )

    def delete_item(self, item_id):
        log.info(f'Delte Item {self.__class__.__name__}')
        try:
            db: Session = db_connection
            db = next(db())
            item = db.query(self.model).filter(self.model.id == item_id)

            if not item.first():
                return {"msg": "usuario no encontrado"}
            item.delete(synchronize_session=False)
            db.commit()
            return {"msg": "usuario eliminado correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al eliminar a la BD " + str(e)
            )

    def filter_and_paginate(self, json_data=None):
        log.info(f'Filter and paginate Items {self.__class__.__name__}')
        """
        EJEMPLO DE ENTRADA:
        json_data= [
            {"username": "diego",'type': 'like'},
            {"username": "diego",'type': '=='},
            {"telefono": ['64440467', '64440469'],'type': 'in'},
            {"apellido": '','type': '!='},
            {"creacion": [10/12/1997,10/12/1997]} // [10/12/1997,None]// [None,10/12/1997]// [10/12/1997]  ,
            {"limit": "2"},
            {"offset": "0"}
            ]
        SALIDA:
            ITEMS, LIMIT, OFFSET
        """
        try:
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
                    for obj in json_data:
                        keys = list(obj.keys())
                        column = getattr(self.model, keys[0], None)
                        if column is not None:
                            if column.type.python_type is datetime:
                                start_date = None
                                end_date = None
                                if len(obj[keys[0]]) == 1:
                                    start_date = obj[keys[0]][0]
                                elif len(obj[keys[0]]) == 2:
                                    start_date, end_date = obj[keys[0]]

                                if start_date and end_date:
                                    query = query.filter(
                                        column.between(start_date, end_date))
                                elif start_date:
                                    query = query.filter(column >= start_date)
                                elif end_date:
                                    query = query.filter(column <= end_date)
                                else:
                                    raise HTTPException(
                                        status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f"el formato del filtro de data es incorrecto se requiere [date_start, date_end] o [null, date_end] o [date]"
                                    )
                            elif 'type' in obj:
                                if obj['type'] == '==':
                                    query = query.filter(
                                        column == obj[keys[0]])
                                elif obj['type'] == 'like':
                                    query = query.filter(
                                        cast(column, sqlalchemy.String).like(f"%{str(obj[keys[0]])}%"))
                                elif obj['type'] == '!=':
                                    query = query.filter(
                                        column != obj[keys[0]])
                                elif obj['type'] == 'in':
                                    typeobj = obj[keys[0]]
                                    if isinstance(typeobj, list):
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

                limit_obj = [obj for obj in json_data if "limit" in obj]
                offset_obj = [obj for obj in json_data if "offset" in obj]
                if limit_obj and offset_obj:
                    limit = limit_obj[0]['limit']
                    offset = offset_obj[0]['offset']
                    try:
                        items = query.offset(
                            offset).limit(limit).all()
                    except:
                        pass
                else:
                    items = query.all()
            else:
                items = query.all()
            return items, limit, offset
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al filtrar en la BD " + str(e)
            )
