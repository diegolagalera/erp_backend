from fastapi import HTTPException, Depends, status
from db.models.user import User
from apis.basic_user_auth import current_user
from typing import List
import logging
log = logging.getLogger("app")


class RoleChecker:
    def __init__(self, required_permissions: List[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: User = Depends(current_user)) -> bool:
        log.info('VERIFICANDO SI TIENES ACCESO A LA RUTA')
        if all(item is None for item in self.required_permissions):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='LAS CONSTANTES DE ROLES NO ESTAN CARGADAS'
            )
        if (len(user.role) != 0):
            for r_perm in self.required_permissions:
                if r_perm in user.role:  # si el usuario tiene tan solo 1  de esos roles para acceder a esa ruta podra verla
                    return True

                # if r_perm not in user.role:
                #     raise HTTPException(
                #         status_code=status.HTTP_401_UNAUTHORIZED,
                #         detail='NO TIENES PERMISOS'
                #     )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='NO TIENES PERMISOS'
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='NO TIENES PERMISOS, TIENE QUE ASIGNAR ALGUN ROL AL USUARIO PARA ACCEDER AL APP'
            )
