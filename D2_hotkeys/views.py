from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from run_counter import RunCoutner

import tkinter as tk
import customtkinter as ctk
import queue
from ctypes import windll, wintypes
from threading import Thread


ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('green')


class Views:
    def __init__(self, run_counter: RunCoutner) -> None:
        self._run_counter = run_counter
        self._queue = queue.Queue()

        self._root = ctk.CTk()

        self._overlay_on = True
        self._overlay_lbl = None

        self._font_h_1 = ('Consolas', 20, 'bold')
        self._font_h_2 = ('Consolas', 18, 'bold')
        self._font_l = ('Consolas', 15, 'normal')
        self._color = '#2FA572'
        self._hover_color = '#106A43'

        self._create_overlay()
        self._preview_loot()

        self._root.after(100, self._process_queue)

    def run_main_view(self):
        self.update_runs()
        self._root.mainloop()

    def _process_queue(self):
        while not self._queue.empty():
            message = self._queue.get_nowait()
            if message == 'insert_loot':
                self._insert_loot()
            elif message == 'preview_loot':
                self._preview_loot_top.deiconify()
            elif message == 'toggle_overlay':
                self._toggle_overlay()
            elif message == 'close_views':
                self._root.destroy()

        self._root.after(100, self._process_queue)

    def insert_loot(self):
        self._queue.put('insert_loot')

    def _insert_loot(self):
        def close_top():
            top.destroy()

        def add_item():
            self._run_counter.add_loot(inpt.get())
            close_top()
            self.update_runs()

        top = ctk.CTkToplevel(self._root)
        top.title('Add Loot')
        top.resizable(False, False)
        top.attributes('-topmost', True)

        inpt = ctk.CTkEntry(top, width=250)
        inpt.pack(side=tk.LEFT, fill=tk.X, expand=tk.TRUE)

        ctk.CTkButton(
            top, text='Add Item', command=add_item, width=50
        ).pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=tk.TRUE
        )
        top.deiconify()
        top.protocol('WM_DELETE_WINDOW', close_top)

    def preview_loot(self):
        self._queue.put('preview_loot')

    def _preview_loot(self):
        def close_top():
            self._preview_loot_top.withdraw()

        self._preview_loot_top = ctk.CTkToplevel(self._root)
        self._preview_loot_top.title('Previewing Looted Items')
        self._preview_loot_top.resizable(False, False)
        self._preview_loot_top.attributes('-topmost', True)

        loot_fr = ctk.CTkScrollableFrame(
            self._preview_loot_top, height=600, width=300,
            scrollbar_button_color=self._color,
            scrollbar_button_hover_color=self._hover_color
        )
        loot_fr.pack(
            side=tk.LEFT, fill=tk.X, expand=tk.TRUE
        )

        for loot in self._run_counter.loot:
            ctk.CTkLabel(
                loot_fr, text=loot, fg_color='transparent'
            ).pack(side=tk.TOP, fill=tk.X, expand=tk.TRUE)

        self._preview_loot_top.protocol('WM_DELETE_WINDOW', close_top)
        self._preview_loot_top.withdraw()

    def _create_overlay(self):
        # Position the overlay
        width = 200
        height = 200
        x = 10
        y = width + 10
        self._root.geometry(f'{width}x{height}+{x}+{y}')

        self._root.overrideredirect(True)
        self._root.resizable(False, False)
        self._root.attributes('-topmost', True)

        self._overlay_lbl = ctk.CTkLabel(
            self._root, text='Runs #', text_color=self._color, font=self._font_h_1
        )
        self._overlay_lbl.pack(side=tk.TOP, fill=tk.X, expand=tk.FALSE)

        ctk.CTkLabel(
            self._root, text='Last 5 looted items:', text_color=self._color, font=self._font_h_2
        ).pack(side=tk.TOP, fill=tk.X, expand=tk.FALSE, pady=(10, 0))

        self._last_5_loots = ctk.CTkFrame(self._root, fg_color='transparent')
        self._last_5_loots.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

        # Make clickthrough
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        hwnd = windll.user32.GetParent(self._root.winfo_id())
        current_style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        new_style = current_style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
        windll.user32.SetLayeredWindowAttributes(hwnd, 0, 200, 0x2)

    def toggle_overlay(self):
        self._queue.put('toggle_overlay')

    def _toggle_overlay(self):
        if self._overlay_on:
            self._overlay_on = False
            self._root.withdraw()
        else:
            self._overlay_on = True
            self._root.deiconify()

    def close_all_views(self):
        self._queue.put('close_views')

    def update_runs(self):
        if not self._overlay_lbl and not isinstance(self._overlay_lbl, ctk.CTkLabel):
            return

        self._overlay_lbl.configure(text=f'Run {self._run_counter.runs}')

        for widget in self._last_5_loots.winfo_children():
            widget.destroy()

        for loot in self._run_counter.loot[:-6:-1]:
            ctk.CTkLabel(
                self._last_5_loots, text=loot, text_color=self._color, font=self._font_l
            ).pack(
                side=tk.TOP, fill=tk.X, expand=tk.FALSE
            )

        self._root.update()
