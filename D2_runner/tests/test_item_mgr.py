import pytest

from managers import ItemMgr
from entities import Item


@pytest.fixture
def item_mgr() -> ItemMgr:
    item_mgr = ItemMgr()
    return item_mgr


def test_item_manager_content(item_mgr: ItemMgr) -> None:
    '''Validate the item manager object content.'''
    # Parameters
    assert hasattr(item_mgr, '_all_items') and item_mgr._all_items == []

    # Properties
    assert hasattr(item_mgr, 'all_items') and item_mgr.all_items == []

    # Methods
    assert hasattr(item_mgr, 'create_item')
    assert hasattr(item_mgr, 'delete_item')
    assert hasattr(item_mgr, 'get_item')


def test_item_mgr_create_item(item_mgr: ItemMgr) -> None:
    '''Test creating new item'''
    assert item_mgr.all_items == []

    item_1 = item_mgr.create_item(description='some random item')
    item_2 = item_mgr.create_item(description='some random item')
    assert isinstance(item_1, Item) and item_1 in item_mgr.all_items
    assert isinstance(item_2, Item) and item_2 in item_mgr.all_items


def test_item_mgr_del_item(item_mgr: ItemMgr) -> None:
    '''Test deleting an existing item'''
    assert item_mgr.all_items == []
    item_1 = item_mgr.create_item(description='some random item')
    assert isinstance(item_1, Item) and item_1 in item_mgr.all_items

    item_mgr.delete_item(item_id=item_1.item_id)
    assert item_1 not in item_mgr.all_items


def test_item_mgr_get_item(item_mgr: ItemMgr) -> None:
    '''Test get an existing item'''
    assert item_mgr.all_items == []
    item_1 = item_mgr.create_item(description='some random item')
    assert isinstance(item_1, Item) and item_1 in item_mgr.all_items

    item_found = item_mgr.get_item(item_id=item_1.item_id)
    assert item_found and item_found is item_1 and item_found in item_mgr.all_items
