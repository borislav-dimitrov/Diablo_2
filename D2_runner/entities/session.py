from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Run

from utils import timedelta_to_str


class Session:
    def __init__(self, sess_id: str):
        self.sess_id = sess_id
        self.runs: list[Run] = []

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
                (fastest.run_time_seconds + slowest.run_time_seconds) / 2
            )
            return [fastest.run_time_stamp, slowest.run_time_stamp, average]

        return results

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
