from sqlalchemy.orm import Session, sessionmaker
from config.database import db_connection
from db.models.role import Role

# esto es de testeo para crear datos por defecto al crear la tabla 
def create_data():
    new_role = Role(name="admin", constant='ADMIN', )
    new_role2 = Role(name="user", constant='USER', )
    db: Session = db_connection
    db = next(db())
    roles = db.query(Role).all()
    if not roles:
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        db.add(new_role2)
        db.commit()
        db.refresh(new_role2)