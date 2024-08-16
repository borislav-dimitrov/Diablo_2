import pytest
import os

from managers import DataMgr


@pytest.fixture
def data_mgr() -> DataMgr:
    data_mgr = DataMgr()
    return data_mgr


def test_save(data_mgr) -> None:
    '''Test the data manager save functionality'''
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

    all_paths = data_mgr.save()
    for folder_path in all_paths['folders']:
        assert os.path.exists(folder_path)

    for file_path in all_paths['files']:
        assert os.path.isfile(file_path)


def test_load(data_mgr) -> None:
    '''Test the data manager load functionality'''
    assert False
