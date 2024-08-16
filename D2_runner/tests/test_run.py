import pytest
import time

from entities import Run
from utils import RunStates


@pytest.fixture
def run() -> Run:
    new_run = Run(run_id='asdiads1')
    return new_run


def test_run_content(run):
    '''Validate the run object content.'''
    # Parameters
    assert hasattr(run, 'run_id') and run.run_id == 'asdiads1'
    assert hasattr(run, '_state') and run._state is RunStates.INITIALIZED
    assert hasattr(run, '_start_time') and run._start_time is None
    assert hasattr(run, '_finish_time') and run._finish_time is None
    assert hasattr(run, '_timestamp_format') and run._timestamp_format == '%H:%M:%S'
    assert hasattr(run, '_run_time_stamp') and run._run_time_stamp is None
    assert hasattr(run, '_run_time_seconds') and run._run_time_seconds is None
    assert hasattr(run, 'loot') and run.loot == []

    # Properties
    assert hasattr(run, 'start_time') and run.start_time is None
    assert hasattr(run, 'finish_time') and run.finish_time is None
    assert hasattr(run, 'run_time_stamp') and run.run_time_stamp is None
    assert hasattr(run, 'run_time_seconds') and run.run_time_seconds is None
    assert hasattr(run, 'state') and run.state is RunStates.INITIALIZED


    # Methods
    assert hasattr(run, 'start_run') and callable(run.start_run)
    assert hasattr(run, 'finish_run') and callable(run.finish_run)
    assert hasattr(run, '_calc_run_time') and callable(run._calc_run_time)


def test_start_run(run):
    '''Test the start run function.'''
    run.start_run()
    assert run.start_time is not None
    assert run.state is RunStates.STARTED


def test_finish_run(run):
    '''Test the finish run function.'''
    run.start_run()
    time.sleep(1)
    run.finish_run()
    assert run.start_time is not None
    assert run.finish_time is not None
    assert run.start_time != run.finish_time
    assert run.state is RunStates.FINISHED


def test_calc_run_time(run):
    '''Test the calculation of the runtime after finishing the run.'''
    run.start_run()
    time.sleep(1)
    run.finish_run()

    assert run._run_time_seconds is not None
    assert run.run_time_seconds is not None
    assert run._run_time_stamp is not None
    assert run.run_time_stamp is not None
    assert run._run_time_stamp is run.run_time_stamp
