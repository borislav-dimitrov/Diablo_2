from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities import Session

import os
import pickle


class DataMgr:
    def __init__(self, data_dir: str = os.path.abspath('data')) -> None:
        self.data_dir = data_dir

    def save(self, sessions: list[Session]) -> list[str]:
        '''Save the existing objects to the file system.'''
        if not sessions:
            return

        all_file_paths = []

        for session in sessions:
            session_file_path = os.path.join(
                self.data_dir, f'sess_{session.sess_id}'
            )
            all_file_paths.append(session_file_path)

            with open(session_file_path, 'wb') as fh:
                pickle.dump(session, fh)

        return all_file_paths

    def load(self) -> list[Session]:
        '''Load objects from the file system.'''
        sessions = []

        for file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file)

            with open(file_path, 'rb') as fh:
                sessions.append(pickle.load(fh))

        return sessions
