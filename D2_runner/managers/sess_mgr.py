from entities import Session, Run
from utils import generate_uniq_id


class SessMgr:
    def __init__(self):
        self._all_sessions: list[Session] = []

    def create_session(self) -> Session:
        '''Create and return a new session.'''
        session = Session(sess_id=generate_uniq_id())
        self._all_sessions.append(session)
        return session

    def delete_session(self, sess_id: str) -> None:
        '''Find and delete the session with the specified ID if it exists.'''
        sess_found = self.get_session(sess_id=sess_id)
        if not sess_found:
            raise RuntimeError(f'No such Run - {sess_id}!')

        self._all_sessions.remove(sess_found)

    def get_session(self, sess_id: str) -> Session:
        '''Find and return the session with the specified ID if it exists.'''
        for session in self._all_sessions:
            if session.sess_id == sess_id:
                return session

    def add_run_to_session(self, run: Run, session: Session) -> Session:
        '''Add run to the specified session.'''
        if session not in self._all_sessions:
            raise RuntimeError(f'Invalid specified session - {session.sess_id}!')

        for sess_run in session.runs:
            if sess_run.run_id == run.run_id:
                raise RuntimeError(f'This run is already in the specified session!')

        session.runs.append(run)
        return session

    @property
    def all_sessions(self) -> list[Session]:
        '''Get all existing sessions'''
        return self._all_sessions
