from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities import Run

from datetime import timedelta
from utils import timedelta_to_str, smaller_time_stamp


class Session:
    def __init__(self, sess_id: str):
        self.sess_id = sess_id
        self.runs: list[Run] = []
        self._sess_started = None
        self._sess_ended = None
        self._sess_duration = None

    def _calc_run_times(self) -> list[str, str, str]:
        '''Calculate the [fastest, slowest, average] run times.'''
        results = ['unknown', 'unknown', 'unknown']
        all_run_times = []

        for run in self.runs:
            all_run_times.append({
                'run': run,
                'delta': run.run_time_seconds
            })

        if self.runs and len(all_run_times) > 1:
            fastest = min(self.runs, key=lambda x: x.run_time_seconds)
            slowest = max(self.runs, key=lambda x: x.run_time_seconds)
            average = timedelta_to_str(
                (
                    timedelta(seconds=fastest.run_time_seconds)
                    + timedelta(seconds=slowest.run_time_seconds)
                ) / 2
            )
            return [fastest.run_time_stamp, slowest.run_time_stamp, average]

        return results

    def end_session(self) -> None:
        '''End the current session.'''
        first, last = self.first_last_runs
        self._sess_started = first.start_time
        self._sess_ended = last.finish_time
        # TODO - implement sess duration and update values on end session

    @property
    def fastest_run(self) -> str:
        '''Get the fastest run time.'''
        return self._calc_run_times()[0]

    @property
    def slowest_run(self) -> str:
        '''Get the slowest run time.'''
        return self._calc_run_times()[1]

    @property
    def average_run(self) -> str:
        '''Get the average run time.'''
        return self._calc_run_times()[2]

    @property
    def runs_count(self) -> int:
        '''Get the ammount of completed runs.'''
        return len(self.runs)

    @property
    def first_last_runs(self) -> list[Run, Run]:
        '''Get the first and the last runs.'''
        if not self.runs:
            return [None, None]

        first_obj = self.runs[0]
        last_obj = self.runs[0]

        for run in self.runs:
            started_at = run.start_time
            first_started_at = first_obj.start_time
            last_started_at = last_obj.start_time

            if smaller_time_stamp(started_at, first_started_at) == started_at:
                first_obj = run
            elif smaller_time_stamp(started_at, last_started_at) == last_started_at:
                last_obj = run

        return first_obj, last_obj
