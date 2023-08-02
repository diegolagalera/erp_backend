
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
        print('ooll')
        print(self.db)
        itemCtr = self.modelCtr(db=self.db)
        return itemCtr.get_item(item_id)

    def create_item(self, item):
        log.info(f'Create Item {self.__class__.__name__}')
        itemCtr = self.modelCtr(db=self.db)
        response = itemCtr.create_item(item.dict())
        return response

    def update_item(self, user_id: int):
        log.info(f'Update Item {self.__class__.__name__}')
        itemCtr = self.modelCtr(self.updateSchema)
        return itemCtr.update_item(user_id)

    def delete_item(self, item_id: int):
        log.info(f'Delte Item {self.__class__.__name__}')
        itemCtr = self.modelCtr()
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
