from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from customtkinter import StringVar

from .timer import Timer
from .run import Run

from datetime import timedelta
from utils import timedelta_to_timestmap, seconds_to_time_stamp


class Session:
    def __init__(self, sess_id: str, timer_lbl_str_var: StringVar):
        self._running = False
        self.sess_id = sess_id
        self.runs: list[Run] = []
        self._timer = Timer(timer_lbl_str_var)

    def _calc_run_times(self) -> list[str, str, str]:
        '''Calculate the [fastest, slowest, average] run times.'''
        results = ['unknown', 'unknown', 'unknown']

        if self.runs and len(self.runs) > 1:
            fastest = min(self.runs, key=lambda x: x.run_time_seconds)
            slowest = max(self.runs, key=lambda x: x.run_time_seconds)
            average = timedelta_to_timestmap(
                (
                    timedelta(seconds=fastest.run_time_seconds)
                    + timedelta(seconds=slowest.run_time_seconds)
                ) / 2
            )
            return [fastest.run_time_stamp, slowest.run_time_stamp, average]

        return results

    def start_session(self) -> None:
        '''Start the session timer.'''
        self._running = True
        self._timer.start_timer()

    def end_session(self) -> None:
        '''End the current session.'''
        self._running = False
        self._timer.stop_timer()

    def add_run(self, run: Run) -> None:
        '''Add a run to the current session.'''
        if not isinstance(run, Run):
            raise RuntimeError('Not a valid Run!')

        if run in self.runs:
            raise RuntimeError('Run is already in current Session!')

        self.runs.append(run)

    @property
    def fastest_run(self) -> str:
        '''Get the fastest run time.'''
        stamp = min(self.runs, key=lambda x: x.run_time_seconds).run_time_stamp
        return stamp

    @property
    def slowest_run(self) -> str:
        '''Get the slowest run time.'''
        stamp = max(self.runs, key=lambda x: x.run_time_seconds).run_time_stamp
        return stamp

    @property
    def average_run(self) -> str:
        '''Get the average run time.'''
        total_time = 0
        for run in self.runs:
            total_time += run.run_time_seconds

        avg_run_time_seconds = int(total_time / len(self.runs))
        return seconds_to_time_stamp(avg_run_time_seconds)

    @property
    def runs_count(self) -> int:
        '''Get the ammount of completed runs.'''
        return len(self.runs)

    @property
    def running(self) -> bool:
        '''Get the running state of the session.'''
        return self._running
