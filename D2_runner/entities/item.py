from utils import ItemCategory


class Item:
    def __init__(
        self, item_id: str, category: ItemCategory,
        description: str, screenshot: str | None = None
    ) -> None:
        self.item_id = item_id
        self.category = category
        self.description = description
        self.screenshot = screenshot
