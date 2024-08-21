from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .app import App

import customtkinter as ctk
import tkinter as tk

from entities import Session, Run, Item
from utils import Themes, FONTS, THEME_COLORS, generate_uniq_id, ItemCategory


class TimersTab:
    def __init__(
        self, theme: Themes, app: App,
        frame: ctk.CTkFrame | ctk.CTkScrollableFrame
    ) -> None:
        self._app = app
        self._frame = frame

        # Style
        self._color_normal = THEME_COLORS[theme]['normal']
        self._color_hover = THEME_COLORS[theme]['hover']

        # Variables
        self._sess_ongoing = None
        self._run_ongoing = None
        self._sess_time = ctk.StringVar(value='00:00:00')
        self._run_time = ctk.StringVar(value='00:00:00')
        self._fastest_time = ctk.StringVar(value='00:00:00')
        self._slowest_time = ctk.StringVar(value='00:00:00')
        self._avg_time = ctk.StringVar(value='00:00:00')
        self._run_count = ctk.StringVar(value=f'{"0":<{len(self._sess_time.get())}}')

        self._create_and_assemble()

    def update_runs_count(self) -> None:
        '''Change the runs counter.'''
        runs_count = self._sess_ongoing.runs_count
        self._run_count.set(value=f'{runs_count:<{len(self._sess_time.get())}}')

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
        self._create_generic_timer(clocks_fr, 'Finished Runs:', self._run_count, pad_y=None)
        self._create_generic_timer(clocks_fr, 'Run Time:', self._run_time, pad_y=None)
        self._create_generic_timer(clocks_fr, 'Fastest Run:', self._fastest_time, pad_y=(20,0))
        self._create_generic_timer(clocks_fr, 'Slowest Run:', self._slowest_time, pad_y=None)
        self._create_generic_timer(clocks_fr, 'Average Run:', self._avg_time, pad_y=None)

        # Controls
        controls_fr = ctk.CTkFrame(self._frame, fg_color='transparent')
        controls_fr.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=10)

        self._start_run_btn = ctk.CTkButton(
            controls_fr, text='Start', width=70, command=self.start_run
        )
        self._start_run_btn.pack(side=tk.LEFT, fill=tk.X, expand=tk.FALSE, padx=30)
        self._start_run_btn.configure(state=tk.NORMAL)

        self._stop_run_btn = ctk.CTkButton(
            controls_fr, text='Stop', width=70, command=self.stop_run
        )
        self._stop_run_btn.pack(side=tk.LEFT, fill=tk.X, expand=tk.FALSE, padx=10)
        self._stop_run_btn.configure(state=tk.DISABLED)

        self._end_sess_btn = ctk.CTkButton(
            controls_fr, text='End Session', width=90, command=self.end_session
        )
        self._end_sess_btn.pack(side=tk.RIGHT, fill=tk.X, expand=tk.FALSE, padx=30)
        self._end_sess_btn.configure(state=tk.DISABLED)
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
            self._frame, text='Add Item to the selected Run', command=self.add_item_to_run
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

    def _add_run_to_runs_section(self, new_run: Run) -> None:
        '''Add run to the runs section.'''
        assert hasattr(self, '_runs_scrl_fr')
        run_count = self._sess_ongoing.runs_count
        base_fr = ctk.CTkFrame(self._runs_scrl_fr, fg_color='transparent')
        base_fr.run_obj = new_run
        base_fr.is_selected = False
        base_fr.pack(side=tk.TOP, fill=tk.X, padx=10)

        run_nr_lbl = ctk.CTkLabel(
            base_fr, text=f'Run {run_count:>{len(self._sess_time.get())}}:',
            anchor=tk.W, text_color=self._color_normal, font=FONTS['label']
        )
        run_nr_lbl.is_selected = False
        run_nr_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        timer_lbl = ctk.CTkLabel(
            base_fr, text=new_run.run_time_stamp, anchor=tk.E,
            text_color=self._color_normal, font=FONTS['label']
        )
        timer_lbl.is_selected = False
        timer_lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        self._runs_scrl_fr.update_idletasks()
        self._runs_scrl_fr._parent_canvas.yview_moveto(1.0)

        widgets = {
            'frame': base_fr,
            'run_nr': run_nr_lbl,
            'timer': timer_lbl
        }

        base_fr.bind('<Button-1>', lambda e: self._select_run(e, widgets))
        base_fr.bind('<Enter>', lambda e: self._run_enter(e, widgets))
        base_fr.bind('<Leave>', lambda e: self._run_leave(e, widgets))

        for widget in base_fr.winfo_children():
            widget.bind('<Button-1>', lambda e: self._select_run(e, widgets))
            widget.bind('<Enter>', lambda e: self._run_enter(e, widgets))
            widget.bind('<Leave>', lambda e: self._run_leave(e, widgets))

    def start_run(self) -> None:
        '''Start a new run.'''
        if self._run_ongoing:
            raise RuntimeError('There is an ongoing run already!')

        # Create run and session(if needed)
        if not self._sess_ongoing:
            self._start_new_session()
        if not self._sess_ongoing.is_running:
            self._sess_ongoing.start_session()

        self._start_new_run()

    def stop_run(self) -> None:
        '''Stop the currently going run.'''
        if not self._run_ongoing:
            raise RuntimeError('You have to start a run first!')

        self._run_ongoing.finish_run()
        self._sess_ongoing.add_run(self._run_ongoing)
        self.update_runs_count()
        self._add_run_to_runs_section(self._run_ongoing)
        self._run_ongoing = None

        self._toggle_run_btns(start=False)
        self._end_sess_btn.configure(state=tk.NORMAL)

    def end_session(self) -> None:
        '''End the current session'''
        if not self._sess_ongoing:
            raise RuntimeError('There is no existing session to be stopped!')
        if not self._sess_ongoing.is_running:
            raise RuntimeError('The current session is not started yet!')

        self._stop_run_btn.configure(state=tk.DISABLED)
        self._sess_ongoing.end_session()
        self._fastest_time.set(self._sess_ongoing.fastest_run)
        self._slowest_time.set(self._sess_ongoing.slowest_run)
        self._avg_time.set(self._sess_ongoing.average_run)
        self._app.data_mgr.save(sessions=[self._sess_ongoing])

        self._sess_ongoing = None

    def add_item_to_run(self) -> None:
        '''Add item to the selected run'''
        # TODO - get selected run
        item = Item(
            item_id=generate_uniq_id(),
            category=ItemCategory.UNKNOWN,
            description='40ed/15ias'
        )
        import pdb; pdb.set_trace()

    def _start_new_session(self) -> Session:
        '''Start a new session.'''
        self._sess_ongoing = Session(
            sess_id=generate_uniq_id(), timer_lbl_str_var=self._sess_time
        )
        self._cleanup()

    def _start_new_run(self) -> Run:
        '''Start a new run.'''
        self._run_ongoing = Run(
            run_id=generate_uniq_id(), timer_lbl_str_var=self._run_time
        )
        self._run_ongoing.start_run()
        self._toggle_run_btns(start=True)

    def _toggle_run_btns(self, start: bool = True) -> None:
        '''Toggle the run button state.'''
        if start:
            self._start_run_btn.configure(state=tk.DISABLED)
            self._stop_run_btn.configure(state=tk.NORMAL)
        else:
            self._start_run_btn.configure(state=tk.NORMAL)
            self._stop_run_btn.configure(state=tk.DISABLED)

    def _cleanup(self) -> None:
        '''Do the cleanup when a new session is started.'''
        self._sess_time.set('00:00:00')
        self.update_runs_count()
        self._run_time.set('00:00:00')

        self._fastest_time.set('00:00:00')
        self._slowest_time.set('00:00:00')
        self._avg_time.set('00:00:00')

        for widget in self._runs_scrl_fr.winfo_children():
            widget.destroy()

    def _select_run(self, _, widgets: dict) -> Run:
        '''Select a run from the scrolling frame with runs.'''
        for top_widget in self._runs_scrl_fr.winfo_children():
            for widget in top_widget.winfo_children():
                widget.configure(bg_color='transparent')
                widget.is_selected = False
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color=self._color_normal)

        for widget in widgets:
            widgets[widget].configure(bg_color=self._color_normal)
            if isinstance(widgets[widget], ctk.CTkLabel):
                widgets[widget].configure(text_color='white')
            widgets[widget].is_selected = True

    def _run_enter(self, _, widgets: dict) -> None:
        '''On run mouse enter.'''
        for widget in widgets:
            if hasattr(widgets[widget], 'is_selected') and not widgets[widget].is_selected:
                widgets[widget].configure(bg_color=self._color_hover)

    def _run_leave(self, _, widgets: dict) -> None:
        '''On run mouse leave.'''
        for widget in widgets:
            if hasattr(widgets[widget], 'is_selected') and not widgets[widget].is_selected:
                widgets[widget].configure(bg_color='transparent')
