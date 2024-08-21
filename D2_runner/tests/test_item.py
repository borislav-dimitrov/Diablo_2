import pytest

from entities import Item


@pytest.fixture
def item() -> Item:
    item = Item(item_id='item001', description='40ed/15ias jewel')
    return item


def test_item_content(item):
    '''Validate the item object content.'''
    # Parameters
    assert hasattr(item, 'item_id') and item.item_id == 'item001'
    assert hasattr(item, 'description') and item.description == '40ed/15ias jewel'
    assert hasattr(item, 'screenshot') and item.screenshot is None
