from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Item

from datetime import datetime, timedelta
from utils import RunStates, timedelta_to_str


class Run:
    def __init__(self, run_id: str) -> None:
        '''
        :param run_id: The unique ID of the current run
        '''
        self.run_id = run_id
        self._state = RunStates.INITIALIZED
        self._start_time = None
        self._finish_time = None
        self._timestamp_format = '%H:%M:%S'
        self._run_time_delta = None
        self._run_time = None
        self.loot: list[Item] = []

    def start_run(self) -> None:
        '''Start the run.'''
        self._start_time = datetime.now()
        self._state = RunStates.STARTED

    def finish_run(self) -> None:
        '''Finish the run.'''
        self._finish_time = datetime.now()
        self._state = RunStates.FINISHED
        self._calc_run_time()

    def _calc_run_time(self) -> None:
        '''Calculate the time for which the run was performed.'''
        if self._start_time and self._finish_time:
            self._run_time_delta = (
                max((self._start_time, self._finish_time))
                - min((self._start_time, self._finish_time))
            )
            self._run_time = timedelta_to_str(self._run_time_delta)
            return

        raise RuntimeError('Run is not finished yet!')

    @property
    def state(self) -> RunStates:
        '''Get the current state of the run.'''
        return self._state

    @property
    def start_time(self) -> str | None:
        '''Get the time of starting the run.'''
        if self._start_time:
            return self._start_time.strftime(self._timestamp_format)

    @property
    def finish_time(self) -> str | None:
        '''Get the time of finishing the run.'''
        if self._finish_time:
            return self._finish_time.strftime(self._timestamp_format)

    @property
    def run_time(self) -> str | None:
        '''Get the time for which the run was performed.'''
        return self._run_time

    @property
    def run_time_delta(self) -> timedelta:
        '''Get the timedelta object of the run time'''
        return self._run_time_delta
