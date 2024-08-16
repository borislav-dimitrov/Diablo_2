import os
import json

from .sess_mgr import SessMgr
from .run_mgr import RunMgr
from .item_mgr import ItemMgr


class DataMgr:
    def __init__(self, data_dir: str = os.path.abspath('data')) -> None:
        self.data_dir = data_dir
        self.session_mgr = SessMgr()
        self.run_mgr = RunMgr()
        self.item_mgr = ItemMgr()

    def save(self) -> dict:
        '''Save the existing objects to the file system.'''
        all_paths = {
            'folders': [],
            'files': []
        }
        for session in self.session_mgr.all_sessions:
            # Create session directories
            session_path = os.path.join(self.data_dir, f'sess_{session.sess_id}')
            self._clear_old_create_new(session_path)
            all_paths['folders'].append(session_path)

            # Create run directories
            for run in session.runs:
                run_path = os.path.join(session_path, f'run_{run.run_id}')
                self._clear_old_create_new(run_path)
                all_paths['folders'].append(run_path)

                # Create item files
                for item in run.loot:
                    item_name = f'item_{item.item_id}'
                    item_path = f'{os.path.join(run_path, item_name)}.json'
                    self._clear_old_create_new(item_path, folder=False)
                    all_paths['files'].append(item_path)

                    with open(item_path, 'w') as fh:
                        json.dump(item.__dict__, fh, indent=4)

                # Create the run file
                run_name = f'run_{run.run_id}'
                run_item_path = f'{os.path.join(run_path, run_name)}.json'
                self._clear_old_create_new(run_item_path, folder=False)
                all_paths['files'].append(run_item_path)
                with open(run_item_path, 'w') as fh:
                    run.loot = [item.item_id for item in run.loot]
                    json.dump(run.__dict__, fh, indent=4)
        return all_paths

    def load(self) -> None:
        '''Load objects from the file system.'''
        # TODO - implement
        import pdb; pdb.set_trace()

    def _clear_old_create_new(self, path: str, folder: bool = True) -> None:
        '''Clear the old file/folder if it exists'''
        if folder:
            if os.path.isdir(path):
                os.rmdir(path)
            os.makedirs(path)

        if not folder:
            if os.path.isfile(path):
                os.remove(path)
