import os
import shutil
import json

from .sess_mgr import SessMgr, Session, Run
from .run_mgr import RunMgr, Item
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

    def load(self) -> list[Session]:
        '''Load objects from the file system.'''
        if not os.path.isdir(self.data_dir):
            raise RuntimeError('The data directory could not be found!')

        sessions = []

        for sess_folder_name in os.listdir(self.data_dir):
            sess_folder_path = os.path.join(self.data_dir, sess_folder_name)
            run_objects = []

            for run_folder_name in os.listdir(sess_folder_path):
                run_folder_path = os.path.join(sess_folder_path, run_folder_name)
                run_cfg = None
                loot_cfg_files = []
                loot: list[Item] = []

                for cfg_file_name in os.listdir(run_folder_path):
                    # Recognize files
                    if cfg_file_name.startswith('run_'):
                        run_cfg = os.path.join(run_folder_path, cfg_file_name)
                    elif cfg_file_name.startswith('item_'):
                        loot_cfg_files.append(os.path.join(run_folder_path, cfg_file_name))

                # Parse the files and create the Python objects
                for item_cfg in loot_cfg_files:
                    loot.append(self._parse_saved_item_file(item_cfg))
                run_objects.append(self._parse_saved_run_file(run_cfg, loot))

            sessions.append(self._create_sess_from_parsed_file_obj(sess_folder_path, run_objects))

        return sessions

    def _clear_old_create_new(self, path: str, folder: bool = True) -> None:
        '''Clear the old file/folder if it exists'''
        if folder:
            if os.path.isdir(path):
                shutil.rmtree(path)
            os.makedirs(path)

        if not folder:
            if os.path.isfile(path):
                os.remove(path)

    def _create_sess_from_parsed_file_obj(self, file_path: str, runs: list[Run]) -> Session:
        '''Create session from objects from parsed runs and items files.'''
        if not os.path.isdir(file_path):
            raise RuntimeError(f'Failed creating session - {os.path.basename(file_path)}!')

        session = Session(os.path.basename(file_path)[:-5])
        session.runs = runs
        return session

    def _parse_saved_run_file(self, file_path: str, loot: list[Item]) -> Run:
        '''Parse a saved run file and convert it into Python object.'''
        with open(file_path, 'r') as fh:
            run_content = json.load(fh)

        if not run_content:
            raise RuntimeError(f'Failed parsing run file - {file_path}!')

        run_obj = Run(run_content['run_id'])
        run_obj._state = run_content['_state']
        run_obj._start_time = run_content['_start_time']
        run_obj._finish_time = run_content['_finish_time']
        run_obj._timestamp_format = run_content['_state']
        run_obj._run_time_seconds = run_content['_run_time_seconds']
        run_obj._run_time_stamp = run_content['_run_time_stamp']
        run_obj.loot = loot
        return run_obj

    def _parse_saved_item_file(self, file_path: str) -> Item:
        '''Parse a saved item file and convert it into Python object.'''
        with open(file_path, 'r') as fh:
            item_content = json.load(fh)

        if not item_content:
            raise RuntimeError(f'Failed parsing item file - {file_path}!')

        item = Item(*item_content.values())
        return item
