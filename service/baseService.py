
import logging
log = logging.getLogger("app")


class BaseService():
    modelCtr = None
    updateSchema = None
    db = None

    def __init__(self) -> None:
        pass

    def get_items(self, filter=None):
        log.info(f'Get Items {self.__class__.__name__}')
        itemCtr = self.modelCtr(db=self.db)
        return itemCtr.get_items(filter)

    def get_item(self, item_id: int):
        log.info(f'Get Item {self.__class__.__name__}')
        itemCtr = self.modelCtr(db=self.db)
        return itemCtr.get_item(item_id)

    def create_item(self, item, transaction: bool = False):
        log.info(f'Create Item {self.__class__.__name__}')
        itemCtr = self.modelCtr(db=self.db)
        if type(item) == dict:
            response = itemCtr.create_item(item, transaction=transaction)
        else:
            response = itemCtr.create_item(item.dict())
        return response

    def update_item(self, item_id: int):
        log.info(f'Update Item {self.__class__.__name__}')
        itemCtr = self.modelCtr(updateSchema=self.updateSchema, db=self.db)
        return itemCtr.update_item(item_id)

    def delete_item(self, item_id: int):
        log.info(f'Delte Item {self.__class__.__name__}')
        itemCtr = self.modelCtr(db=self.db)
        return itemCtr.delete_item(item_id)


""" get_items
        ENTRADA: 
        FILTER= [
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
