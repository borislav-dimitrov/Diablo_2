import pytest
import os
import shutil
from typing import Generator

from managers import DataMgr
from entities import Session, Run, Item
from utils import generate_uniq_id


class StringVar:
    def __init__(self):
        pass

    def get(self):
        pass

    def set(self):
        pass


def clear_data_dir(data_mgr: DataMgr) -> None:
    '''Clear the data directory before/after the tests.'''
    for file in os.listdir(data_mgr.data_dir):
        os.remove(os.path.join(data_mgr.data_dir, file))

    assert os.listdir(data_mgr.data_dir) == []


def create_dummy_data() -> list[Session]:
    '''Create dummy data for the tests.'''
    item_1 = Item(item_id=generate_uniq_id(), description='item001')
    item_2 = Item(item_id=generate_uniq_id(), description='item002')
    item_3 = Item(item_id=generate_uniq_id(), description='item003')


    run_1 = Run(generate_uniq_id(), StringVar())
    run_1.add_item(item=item_1)
    run_1.add_item(item=item_3)
    assert item_1 in run_1.loot
    assert item_3 in run_1.loot

    run_2 = Run(generate_uniq_id(), StringVar())
    run_2.add_item(item=item_2)

    sess_1 = Session(generate_uniq_id(), StringVar())
    sess_1.add_run(run=run_1)
    sess_1.add_run(run=run_2)
    assert item_2 in run_2.loot

    assert sess_1.runs != []
    assert run_1.loot != []
    assert run_2.loot != []

    return [sess_1]

@pytest.fixture
def preparation() -> Generator:
    data_mgr = DataMgr(data_dir=os.path.abspath(r'tests\test_data_dir'))
    clear_data_dir(data_mgr)
    yield data_mgr, create_dummy_data()
    clear_data_dir(data_mgr)


def test_save(preparation: list[DataMgr, list[Session]]) -> None:
    '''Test the data manager save functionality'''
    data_mgr, sessions = preparation
    all_paths = data_mgr.save(sessions=sessions)
    assert all_paths

    for file_path in all_paths:
        assert os.path.exists(file_path)

def test_load(preparation: list[DataMgr, list[Session]], sessions = preparation) -> None:
    '''Test the data manager load functionality'''
    data_mgr, sessions = preparation
    data_mgr.save(sessions=sessions)

    sessions = data_mgr.load()
    assert len(sessions) == 1
    assert len(sessions[0].runs) == 2
    assert len(sessions[0].runs[0].loot) == 2
    assert sessions[0].runs[0].loot[0].description == 'item001'
    assert sessions[0].runs[0].loot[1].description == 'item003'
    assert len(sessions[0].runs[1].loot) == 1
    assert sessions[0].runs[1].loot[0].description == 'item002'
