from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from customtkinter import StringVar

from datetime import datetime, timedelta
from utils import RunStates, timedelta_to_timestmap
from .timer import Timer
from .item import Item


class Run:
    def __init__(self, run_id: str, timer_lbl_str_var: StringVar) -> None:
        '''
        :param run_id: The unique ID of the current run
        '''
        self.run_id = run_id
        self._state = RunStates.INITIALIZED
        self._start_time = None
        self._finish_time = None
        self.loot: list[Item] = []

        self._time_stamp = '00:00:00'
        self._timer = Timer(timer_lbl_str_var)

    def start_run(self) -> None:
        '''Start the run.'''
        self._start_time = datetime.now()
        self._state = RunStates.STARTED
        self._timer.start_timer()

    def finish_run(self) -> None:
        '''Finish the run.'''
        self._finish_time = datetime.now()
        self._state = RunStates.FINISHED
        self._timer.stop_timer()
        self._time_stamp = self._timer._str_var.get()

    def add_item(self, item: Item) -> None:
        '''Add item to the current run.'''
        if not isinstance(item, Item):
            raise RuntimeError('Not a valid Item!')

        if item in self.loot:
            raise RuntimeError('Item is already in current Run!')

        self.loot.append(item)

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
    def run_time_stamp(self) -> str | None:
        '''Get the time stamp for which the run was performed.'''
        return self._time_stamp

    @property
    def run_time_seconds(self) -> timedelta:
        '''Get the seconds of the run time'''
        return self._timer.get_seconds
