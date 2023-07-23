
from controller.baseCrud import BaseCrud


class BaseService():
    modelCtr = BaseCrud
    updateSchema = None

    def __init__(self) -> None:
        pass

    def get_items(self, filter=None):
        """
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
        print('controllerrrr')
        print(filter)
        itemCtr = self.modelCtr()
        return itemCtr.get_items(filter)

    def create_item(self, item):
        itemCtr = self.modelCtr()
        response = itemCtr.create_item(item.dict())
        return response

    def get_item(self, item_id: int):
        itemCtr = self.modelCtr()
        return itemCtr.get_item(item_id)

    def update_item(self, user_id: int):
        itemCtr = self.modelCtr(self.updateSchema)
        return itemCtr.update_item(user_id)

    def delete_item(self, item_id: int):
        itemCtr = self.modelCtr()
        return itemCtr.delete_item(item_id)
