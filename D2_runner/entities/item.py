class Item:
    def __init__(
        self, item_id: str, descritpion: str, screenshot: str | None = None
    ) -> None:
        '''
        :param item_id: The unique ID of the current item
        :param description: The description of the current item
        :param screenshot: The path to the screenshot of this item
        '''
        self.item_id = item_id
        self.description = descritpion
        self.screenshot = screenshot
