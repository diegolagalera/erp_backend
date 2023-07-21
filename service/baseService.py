
class BaseService():
    modelCtr = None
    updateSchema = None

    def __init__(self) -> None:
        pass

    def get_items(self):
        itemCtr = self.modelCtr()
        return itemCtr.get_items()

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
