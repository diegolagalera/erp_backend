from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from db.models.user import filter, UserSchema, ShowUserSchema, UpdateUserSchema, ShowUserSchemaPaginate, filterUserParamsSchema
from service.userService import UserService
from service.addressService import AddressService
from config.roleChecker import RoleChecker
from config.roleConstant import ROLES
from fastapi.encoders import jsonable_encoder
from dateutil.parser import parse as parse_datetime
from config.database import db_connection
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
import pdfkit
from controller.sendEmailController import send_email
testApi = APIRouter(
    prefix='/test', tags=["test"], responses={404: {"message": "NO FOUND ROUTA /user"}})

acces_get_ussers = [ROLES['admin'], ROLES['user']]
acces_get_usser = [ROLES['admin']]
acces_create_user = [ROLES['admin']]
acces_update_user = [ROLES['admin'], ROLES['user']]
acces_delete_user = [ROLES['admin'], ]

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("static/templates/template_factura.html")

# @userApi.post("/", response_model=ShowUserSchemaPaginate)


@testApi.post("/generate_pdf_and_send_email")
async def generate_pdf_and_send_email(data: dict):
    # userService = UserService(db=db)
    print(data)
    rendered_html = template.render(data)
    # rendered_html = template.render()

    pdf_file_path = "static/templates/fresultfile.pdf"
    print('iiiiiiiiiiiiiiiiiiiiiiii')
    pdfkit.from_string(rendered_html, pdf_file_path)
    # SEND EMAIL
    sender_email = "diegolagalera12@gmail.com"
    sender_password = "tnbkiasddlhhryaq"
    receiver_email = data.get('receiver_email', 'diegolagalera_@hotmail.com')
    subject = "Reporte PDF generado con FastAPI"
    body = "Adjuntamos el PDF generado con FastAPI. ¡Gracias por usar nuestra plataforma!"
    send_email(sender_email, sender_password, receiver_email, subject, body, pdf_file_path)

    return status.HTTP_200_OK


@testApi.delete("/delete", dependencies=[Depends(RoleChecker(acces_delete_user))])
def delete_address(user_id: int, db: Session = Depends(db_connection)):
    addressService = AddressService(db=db)
    return addressService.delete_item(user_id)
