from controller.baseController import BaseController
from db.models.orders import Order
# from sqlalchemy.orm import Session
# from config.database import db_connection
from sqlalchemy import or_
from schemas.OrderSchemas import ShowOrderSchema, UpdateOrderSchema


class OrderController(BaseController):
    model = Order
    updateSchema = None

    def __init__(self, updateSchema=None):
        self.updateSchema = updateSchema

    def create_item(self, item, user: ShowOrderSchema):
        try:
            # db: Session = db_connection
            item = item.dict()
            new_order = Order(**item)
            new_order.user = user
            return super().create_item(new_order,True)
        except:
            raise

        # return super().create_item(item)


