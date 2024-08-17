import pytest
import os
import shutil
from typing import Generator

from managers import DataMgr


def clear_data_dir(data_mgr: DataMgr) -> None:
    '''Clear the data directory before/after the tests.'''
    for sess_folder in os.listdir(data_mgr.data_dir):
        shutil.rmtree(os.path.join(data_mgr.data_dir, sess_folder))
    assert os.listdir(data_mgr.data_dir) == []


def create_dummy_data(data_mgr: DataMgr) -> None:
    '''Create dummy data for the tests.'''
    item_1 = data_mgr.item_mgr.create_item(description='item001')
    assert item_1 in data_mgr.item_mgr.all_items
    item_2 = data_mgr.item_mgr.create_item(description='item002')
    assert item_2 in data_mgr.item_mgr.all_items
    item_3 = data_mgr.item_mgr.create_item(description='item003')
    assert item_3 in data_mgr.item_mgr.all_items
    run_1 = data_mgr.run_mgr.create_run()
    assert run_1 in data_mgr.run_mgr.all_runs
    run_2 = data_mgr.run_mgr.create_run()
    assert run_2 in data_mgr.run_mgr.all_runs
    sess_1 = data_mgr.session_mgr.create_session()
    assert sess_1 in data_mgr.session_mgr.all_sessions

    data_mgr.session_mgr.add_run_to_session(run=run_1, session=sess_1)
    assert run_1 in sess_1.runs
    data_mgr.session_mgr.add_run_to_session(run=run_2, session=sess_1)
    assert run_2 in sess_1.runs

    data_mgr.run_mgr.add_item_to_run(item=item_1, run=run_1)
    assert item_1 in run_1.loot
    data_mgr.run_mgr.add_item_to_run(item=item_3, run=run_1)
    assert item_3 in run_1.loot
    data_mgr.run_mgr.add_item_to_run(item=item_2, run=run_2)
    assert item_2 in run_2.loot

    assert sess_1.runs != []
    assert run_1.loot != []
    assert run_2.loot != []


@pytest.fixture
def data_mgr() -> Generator:
    data_mgr = DataMgr(data_dir=os.path.abspath(r'tests\test_data_dir'))
    clear_data_dir(data_mgr)
    create_dummy_data(data_mgr)
    yield data_mgr
    clear_data_dir(data_mgr)


def test_save(data_mgr: DataMgr) -> None:
    '''Test the data manager save functionality'''
    all_paths = data_mgr.save()
    assert all_paths['folders'] and all_paths['files']

    for folder_path in all_paths['folders']:
        assert os.path.exists(folder_path)

    for file_path in all_paths['files']:
        assert os.path.isfile(file_path)


def test_load(data_mgr: DataMgr) -> None:
    '''Test the data manager load functionality'''
    data_mgr.save()
    sessions = data_mgr.load()
    assert len(sessions) == 1
    assert len(sessions[0].runs) == 2
    assert len(sessions[0].runs[0].loot) == 1
    assert len(sessions[0].runs[1].loot) == 2
