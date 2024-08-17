import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from utils import Themes, FONTS, THEME_COLORS


class TimersTab:
    def __init__(
        self, theme: Themes, frame: ctk.CTkFrame | ctk.CTkScrollableFrame
    ) -> None:
        self._frame = frame

        # Style
        self._color_normal = THEME_COLORS[theme]['normal']
        self._color_hover = THEME_COLORS[theme]['hover']

        # Variables
        self._sess_time = ctk.StringVar(value='00:00:00')
        self._run_time = ctk.StringVar(value='00:00:00')
        self._fastest_time = ctk.StringVar(value='00:00:00')
        self._slowest_time = ctk.StringVar(value='00:00:00')
        self._avg_time = ctk.StringVar(value='00:00:00')
        self._run_count = ctk.StringVar(value=f'{"0":<{len(self._sess_time.get())}}')
        self._runs = []

        self._create_and_assemble()

        for i in range(20):
            self.add_run_to_runs_section(i * 50)

    def change_runs_count(self, count: int) -> None:
        '''Change the runs counter.'''
        assert isinstance(count, int)

        self._run_count = ctk.StringVar(value=f'{count:<{len(self._sess_time.get())}}')

    def _create_and_assemble(self) -> None:
        '''Create and assemble the timers tab.'''
        # region Clocks Frame
        self._clocks_title = ctk.CTkLabel(
            self._frame, text='Clocks', text_color=self._color_normal,
            font=FONTS['header_1']
        )
        self._clocks_title.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        clocks_fr = ctk.CTkFrame(
            self._frame, border_color=self._color_normal, border_width=1,
        )
        clocks_fr.pack_propagate(False)
        clocks_fr.pack(
            side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, padx=10
        )

        self._create_generic_timer(clocks_fr, 'Session Time:', self._sess_time)
        self._create_generic_timer(clocks_fr, 'Runs Count:', self._run_count, pad_y=None)
        self._create_generic_timer(clocks_fr, 'Run Time:', self._run_time, pad_y=None)
        self._create_generic_timer(clocks_fr, 'Fastest Run:', self._fastest_time, pad_y=(20,0))
        self._create_generic_timer(clocks_fr, 'Slowest Run:', self._slowest_time, pad_y=None)
        self._create_generic_timer(clocks_fr, 'Average Run:', self._avg_time, pad_y=None)

        # Controls
        controls_fr = ctk.CTkFrame(self._frame, fg_color='transparent')
        controls_fr.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=10)
        self._start_run_btn = ctk.CTkButton(
            controls_fr, text='Start', width=100,
            command=lambda: print('Starting run...'),
        )
        self._start_run_btn.pack(side=tk.LEFT, fill=tk.X, expand=tk.FALSE, padx=(30, 0))
        self._stop_run_btn = ctk.CTkButton(
            controls_fr, text='Stop', width=100,
            command=lambda: print('Stopping run...')
        )
        self._stop_run_btn.pack(side=tk.RIGHT, fill=tk.X, expand=tk.FALSE, padx=(0, 30))
        # endregion

        # region Runs Frame
        self._runs_title = ctk.CTkLabel(
            self._frame, text='Runs', text_color=self._color_normal,
            font=FONTS['header_1']
        )
        self._runs_title.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, pady=(10,0))
        runs_fr = ctk.CTkFrame(self._frame, border_color=self._color_normal, border_width=1)
        runs_fr.pack_propagate(False)
        runs_fr.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, padx=10)


        # Titles
        titles_font = FONTS['header_3']
        runs_titles_fr = ctk.CTkFrame(
            runs_fr, border_color=self._color_normal, border_width=1, height=20
        )
        runs_titles_fr.pack(side=tk.TOP, fill=tk.X, expand=False, padx=10, pady=(10,0))
        run_lbl = ctk.CTkLabel(
            runs_titles_fr, text='Run Nr.', text_color=self._color_normal, font=titles_font
        )
        run_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=5)
        runs_title_sep = ctk.CTkLabel(
            runs_titles_fr, text='|', text_color=self._color_normal, font=titles_font
        )
        runs_title_sep.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=5)
        run_time_lbl = ctk.CTkLabel(
            runs_titles_fr, text='Run Time', text_color=self._color_normal, font=titles_font
        )
        run_time_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=5)

        self._runs_scrl_fr = ctk.CTkScrollableFrame(
            runs_fr, fg_color='transparent',
            scrollbar_button_color=self._color_normal,
            scrollbar_button_hover_color=self._color_hover
        )
        self._runs_scrl_fr.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=5)

        self._add_item_to_run_btn = ctk.CTkButton(
            self._frame, text='Add Item to the selected Run',
            command=lambda: print('Adding item to...')
        )
        self._add_item_to_run_btn.pack(
            side=tk.TOP, fill=tk.BOTH, expand=tk.FALSE,
            padx=40, pady=10
        )
        # endregion

    def _create_generic_timer(
        self, parent: ctk.CTkFrame, text: str, variable: ctk.StringVar,
        pad_y: tuple = (5, 0)
    ) -> None:
        '''Create generic timer section'''
        assert isinstance(variable, ctk.StringVar)
        assert isinstance(parent, ctk.CTkFrame)

        base_fr = ctk.CTkFrame(parent, fg_color='transparent')
        base_fr.pack(side=tk.TOP, fill=tk.X, padx=(70,), pady=pad_y)

        text_lbl = ctk.CTkLabel(
            base_fr, text=f'{text:>13}', anchor=tk.W,
            text_color=self._color_normal, font=FONTS['label']
        )
        text_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        timer_lbl = ctk.CTkLabel(
            base_fr, textvariable=variable, anchor=tk.W,
            text_color=self._color_normal, font=FONTS['label']
        )
        timer_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

    def add_run_to_runs_section(self, run=None) -> None:
        '''Add run to the runs section.'''
        assert hasattr(self, '_runs_scrl_fr')

        base_fr = ctk.CTkFrame(self._runs_scrl_fr, fg_color='transparent')
        base_fr.pack(side=tk.TOP, fill=tk.X, padx=10)

        run_nr_lbl = ctk.CTkLabel(
            base_fr, text=f'Run {run:>{len(self._sess_time.get())}}:', anchor=tk.W,
            text_color=self._color_normal, font=FONTS['label']
        )
        run_nr_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        timer_lbl = ctk.CTkLabel(
            base_fr, text='00:00:00', anchor=tk.E,
            text_color=self._color_normal, font=FONTS['label']
        )
        timer_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
