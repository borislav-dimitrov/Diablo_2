import pytest

from managers import SessMgr, RunMgr
from entities import Session


@pytest.fixture
def sess_mgr() -> SessMgr:
    sess_mgr = SessMgr()
    return sess_mgr


def test_sess_manager_content(sess_mgr: SessMgr) -> None:
    '''Validate the session manager object content.'''
    # Parameters
    assert hasattr(sess_mgr, '_all_sessions') and sess_mgr._all_sessions == []

    # Properties
    assert hasattr(sess_mgr, 'all_sessions') and sess_mgr.all_sessions == []

    # Methods
    assert hasattr(sess_mgr, 'create_session')
    assert hasattr(sess_mgr, 'delete_session')
    assert hasattr(sess_mgr, 'get_session')
    assert hasattr(sess_mgr, 'add_run_to_session')


def test_sess_mgr_create_session(sess_mgr: SessMgr) -> None:
    '''Test creating new session.'''
    assert sess_mgr.all_sessions == []

    sess_1 = sess_mgr.create_session()
    sess_2 = sess_mgr.create_session()
    assert isinstance(sess_1, Session) and sess_1 in sess_mgr.all_sessions
    assert isinstance(sess_2, Session) and sess_2 in sess_mgr.all_sessions


def test_sess_mgr_del_session(sess_mgr: SessMgr) -> None:
    '''Test deleting an existing session.'''
    assert sess_mgr.all_sessions == []
    sess_1 = sess_mgr.create_session()
    assert isinstance(sess_1, Session) and sess_1 in sess_mgr.all_sessions

    sess_mgr.delete_session(sess_id=sess_1.sess_id)
    assert sess_1 not in sess_mgr.all_sessions


def test_sess_mgr_get_session(sess_mgr: SessMgr) -> None:
    '''Test get an existing session.'''
    assert sess_mgr.all_sessions == []
    sess_1 = sess_mgr.create_session()
    assert isinstance(sess_1, Session) and sess_1 in sess_mgr.all_sessions

    sess_found = sess_mgr.get_session(sess_id=sess_1.sess_id)
    assert sess_found and sess_found is sess_1 and sess_found in sess_mgr.all_sessions


def test_sess_mgr_add_run_to_session(sess_mgr: SessMgr) -> None:
    '''Test adding run to a session.'''
    run_mgr = RunMgr()

    assert sess_mgr.all_sessions == []
    sess_1 = sess_mgr.create_session()
    assert isinstance(sess_1, Session) and sess_1 in sess_mgr.all_sessions

    run_1 = run_mgr.create_run()
    assert run_1 in run_mgr.all_runs

    sess_mgr.add_run_to_session(run=run_1, session=sess_1)
    assert run_1 in sess_1.runs
