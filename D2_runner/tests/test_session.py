import pytest
import time

from entities import Run, Session


@pytest.fixture
def session() -> Session:
    new_session = Session(sess_id='session001')
    return new_session

def test_session_content(session):
    '''Validate the session object content.'''
    # Parameters
    assert hasattr(session, 'sess_id') and session.sess_id == 'session001'
    assert hasattr(session, 'runs') and session.runs == []

    # Properties
    assert hasattr(session, 'fastest_run') and session.fastest_run == 'unknown'
    assert hasattr(session, 'slowest_run') and session.slowest_run == 'unknown'
    assert hasattr(session, 'average_run') and session.average_run == 'unknown'
    assert hasattr(session, 'runs_count') and session.runs_count == 0

    # Methods
    assert hasattr(session, '_calc_run_times')


def test_session_min_max_avg_run_times(session):
    '''Test the session min max avg run times calculation.'''
    run_1 = Run(run_id='run001')
    run_2 = Run(run_id='run002')
    run_3 = Run(run_id='run003')
    run_4 = Run(run_id='run004')
    run_5 = Run(run_id='run005')
    session.runs.append(run_1)
    session.runs.append(run_2)
    session.runs.append(run_3)
    session.runs.append(run_4)
    session.runs.append(run_5)
    run_1.start_run()
    run_2.start_run()
    run_3.start_run()
    run_4.start_run()
    run_5.start_run()

    time.sleep(1.23)
    run_2.finish_run()
    time.sleep(0.32)
    run_5.finish_run()
    time.sleep(.25)
    run_1.finish_run()
    time.sleep(1)
    run_3.finish_run()
    time.sleep(1)
    run_4.finish_run()

    assert session.fastest_run == '00:00:02'
    assert session.slowest_run == '00:00:04'
    assert session.average_run == '00:00:03'
