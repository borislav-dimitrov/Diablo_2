import pytest

from managers import RunMgr, ItemMgr
from entities import Run


@pytest.fixture
def run_mgr() -> RunMgr:
    run_mgr = RunMgr()
    return run_mgr


def test_run_manager_content(run_mgr: RunMgr) -> None:
    '''Validate the run manager object content.'''
    # Parameters
    assert hasattr(run_mgr, '_all_runs') and run_mgr._all_runs == []

    # Properties
    assert hasattr(run_mgr, 'all_runs') and run_mgr.all_runs == []

    # Methods
    assert hasattr(run_mgr, 'create_run')
    assert hasattr(run_mgr, 'delete_run')
    assert hasattr(run_mgr, 'get_run')
    assert hasattr(run_mgr, 'add_item_to_run')


def test_run_mgr_create_item(run_mgr: RunMgr) -> None:
    '''Test creating new item.'''
    assert run_mgr.all_runs == []

    run_1 = run_mgr.create_run()
    run_2 = run_mgr.create_run()
    assert isinstance(run_1, Run) and run_1 in run_mgr.all_runs
    assert isinstance(run_2, Run) and run_2 in run_mgr.all_runs


def test_run_mgr_del_item(run_mgr: RunMgr) -> None:
    '''Test deleting an existing item.'''
    assert run_mgr.all_runs == []
    run_1 = run_mgr.create_run()
    assert isinstance(run_1, Run) and run_1 in run_mgr.all_runs

    run_mgr.delete_run(run_id=run_1.run_id)
    assert run_1 not in run_mgr.all_runs


def test_run_mgr_get_item(run_mgr: RunMgr) -> None:
    '''Test get an existing item.'''
    assert run_mgr.all_runs == []
    run_1 = run_mgr.create_run()
    assert isinstance(run_1, Run) and run_1 in run_mgr.all_runs

    run_found = run_mgr.get_run(run_id=run_1.run_id)
    assert run_found and run_found is run_1 and run_found in run_mgr.all_runs


def test_run_mgr_add_item_to_run(run_mgr: RunMgr) -> None:
    '''Test adding an item to a run.'''
    item_mgr = ItemMgr()

    assert run_mgr.all_runs == []
    run_1 = run_mgr.create_run()
    assert isinstance(run_1, Run) and run_1 in run_mgr.all_runs

    item_1 = item_mgr.create_item(description='some random item1')
    assert item_1 in item_mgr.all_items

    run_mgr.add_item_to_run(item=item_1, run=run_1)
    assert item_1 in run_1.loot
