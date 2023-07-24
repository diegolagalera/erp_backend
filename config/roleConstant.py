from sqlalchemy.orm import Session
from config.database import db_connection
from db.models.role import Role
import logging
log = logging.getLogger("app")
"""
AQUI CARGAMOS TODOS LOS ROLES QUE TENEMOS EN LA BASE DE DATOS PARA PODER UTILIZARLOS AL SISTEMA,
ES OBLIGADO QUE EL ROL QUE ESTA EN BD ESTE EN DECLARADO EN ESTE ARCHIVO COMO NONE
"""
ROLES = {
    'ADMIN': None,
    'USER': None
}


def defineRoleConstant():
    log.info('CARGANDO CONSTANTES DE LA TABLA ROLES AL SISTEMA')
    try:
        db: Session = db_connection
        db = next(db())
        roles = db.query(Role).filter().all()
        if roles:
            for rol in roles:
                ROLES[rol.constant] = rol.id
    except:
        raise
