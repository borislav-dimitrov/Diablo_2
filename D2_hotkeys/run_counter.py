import pickle
import os


class RunCoutner:
    def __init__(self, runs_file='runs.json') -> None:
        self._runs_file = runs_file
        self._runs_ct = 0
        self._loot = []

    def save(self):
        with open(self._runs_file, 'wb') as handle:
            pickle.dump(self, handle)

    def load(self):
        if not os.path.isfile(self._runs_file):
            return

        with open(self._runs_file, 'rb') as handle:
            loaded_obj: RunCoutner = pickle.load(handle)

        if isinstance(loaded_obj, RunCoutner):
            self._runs_ct = loaded_obj.runs
            self._loot = loaded_obj.loot

    def add_loot(self, loot_description: str):
        self._loot.append(f'{loot_description} #{self._runs_ct}')

    @property
    def runs(self):
        return self._runs_ct

    @property
    def loot(self):
        return self._loot
