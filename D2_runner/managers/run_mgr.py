from entities import Run, Item
from utils import generate_uniq_id


class RunMgr:
    def __init__(self) -> None:
        self._all_runs: list[Run] = []

    def create_run(self) -> Run:
        '''Create and return a new run.'''
        run = Run(run_id=generate_uniq_id())
        self._all_runs.append(run)
        return run

    def delete_run(self, run_id: str) -> None:
        '''Find and delete the run with the specified ID if it exists.'''
        run_found = self.get_run(run_id=run_id)
        if not run_found:
            raise RuntimeError(f'No such Run - {run_id}!')

        self._all_runs.remove(run_found)

    def get_run(self, run_id: str) -> Run:
        '''Find and return the run with the specified ID if it exists.'''
        for run in self._all_runs:
            if run.run_id == run_id:
                return run

    def add_item_to_run(self, item: Item, run: Run) -> Run:
        '''Add item to the specified run.'''
        if run not in self._all_runs:
            raise RuntimeError(f'Invalid specified run - {run.run_id}!')

        for run_item in run.loot:
            if run_item.item_id == item.item_id:
                raise RuntimeError(f'This item is already in the specified run!')

        run.loot.append(item)
        return Run

    @property
    def all_runs(self) -> list[Run]:
        '''Get all existing runs'''
        return self._all_runs
