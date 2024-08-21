import customtkinter as ctk
import time
from threading import Thread
from datetime import timedelta

from utils import timedelta_to_timestmap


class Timer:
    def __init__(self, str_var: ctk.StringVar):
        self._str_var = str_var
        self._seconds = 0
        self._running = False

    def start_timer(self) -> None:
        '''Start the timer.'''
        self._running = True
        self._str_var.set(value='00:00:00')
        thread = Thread(target=self._thread_target, args=(), daemon=True)
        thread.start()

    def stop_timer(self) -> None:
        '''Stop the timer.'''
        self._running = False

    def _thread_target(self) -> None:
        '''Do stuff on tick.'''
        while self._running:
            time.sleep(1)
            if self._running:
                self._seconds += 1
                delta = timedelta(seconds=self._seconds)
                self._str_var.set(value=timedelta_to_timestmap(delta))

    @property
    def get_seconds(self) -> int:
        '''Get the ammount of seconds passed.'''
        return self._seconds
