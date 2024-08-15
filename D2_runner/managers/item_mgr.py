from entities import Item
from utils import generate_uniq_id

class ItemMgr:
    def __init__(self):
        self._all_items: list[Item] = []

    def create_item(self, description: str, screenshot: str | None = None) -> Item:
        '''Create and return a new Item.'''
        item = Item(
            item_id=generate_uniq_id(),
            descritpion=description,
            screenshot=screenshot
        )
        self._all_items.append(item)
        return item

    def delete_item(self, item_id: str) -> None:
        '''Find and delete the item with the specified ID if it exists.'''
        item_found = self.get_item(item_id=item_id)
        if not item_found:
            raise RuntimeError(f'No such Item - {item_id}!')

        self._all_items.remove(item_found)

    def get_item(self, item_id: str) -> Item:
        '''Find and return the item with the specified ID if it exists.'''
        for item in self._all_items:
            if item.item_id == item_id:
                return item

    @property
    def all_items(self) -> list[Item]:
        '''Get all existing items'''
        return self._all_items
