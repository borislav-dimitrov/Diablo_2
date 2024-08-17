from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from managers import DataMgr

import os
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from utils import Appearances, Themes, THEME_COLORS
from .timers_tab import TimersTab


class App:
    def __init__(
        self,
        data_manager: DataMgr,
        appearance: Appearances = Appearances.DARK,
        theme: Themes = Themes.GREEN,
        resolution: tuple = (400, 630),
        allow_resize: bool = False,
        title: str = 'Diablo 2 Runner',
        icon: str = r'resources\icon.ico'
    ) -> None:
        self.data_mgr = data_manager
        self._appearance = appearance
        self._theme = theme
        self._resolution = resolution
        self._allow_resize = allow_resize
        self._title = title
        self._icon = os.path.abspath(icon)
        self._app = ctk.CTk()

        self._init()

    def _init(self) -> None:
        '''Initialize the application.'''
        ctk.set_appearance_mode(self._appearance)
        ctk.set_default_color_theme(self._theme)

        self._app.title(self._title)
        self._app.geometry(f'{self._resolution[0]}x{self._resolution[1]}')
        assert os.path.isfile(self._icon)
        self._app.iconbitmap(self._icon)
        if not self._allow_resize:
            self._app.resizable(False, False)

        self._create_gui()

    def _create_gui(self) -> None:
        '''Create and assemble the gui widgets.'''
        self._main_tab_view = ctk.CTkTabview(master=self._app)
        self._main_tab_view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._timers_tab = TimersTab(
            app=self, theme=self._theme,
            frame=self._add_tab_to_main_tab_view('Timers')
        )
        self._review_sess_tab = self._add_tab_to_main_tab_view('Review Session')
        self._grail_tab = self._add_tab_to_main_tab_view('Grail')
        self._options_tab = self._add_tab_to_main_tab_view('Options')
        self._profile_tab = self._add_tab_to_main_tab_view('Profile')
        self._about_tab = self._add_tab_to_main_tab_view('About')

    def _add_tab_to_main_tab_view(
        self, tab_name: str, y_scroll: bool = False
    ) -> ctk.CTkFrame | ctk.CTkScrollableFrame:
        '''Add a new tab to the main tab view.'''
        frame = self._main_tab_view.add(tab_name)

        if y_scroll:
            scrollable_frame = ctk.CTkScrollableFrame(
                frame,
                scrollbar_button_color=THEME_COLORS[self._theme]['normal'],
                scrollbar_button_hover_color=THEME_COLORS[self._theme]['hover']
            )
            scrollable_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            return scrollable_frame
        return frame

    def change_appearance(self, new_appearance: Appearances) -> None:
        '''Change the app appearance.'''
        assert isinstance(new_appearance, Appearances), 'Invalid appearance!'

        self._appearance = new_appearance
        ctk.set_appearance_mode(self._appearance)

    def change_theme(self, new_theme: Themes) -> None:
        '''Change the app theme.'''
        assert isinstance(new_theme, Themes), 'Invalid theme!'

        self._theme = new_theme
        self._timers_tab._color_normal = self._theme
        ctk.set_default_color_theme(self._theme)

    def run(self):
        '''Run the application.'''
        self._app.mainloop()
