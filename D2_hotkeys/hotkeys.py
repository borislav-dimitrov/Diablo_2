from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from run_counter import RunCoutner

import tkinter as tk
import customtkinter as ctk
import pyautogui
import keyboard


ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('green')


class HotKeys:
    def __init__(self) -> None:
        self.inserting_item = False
        self.previewing_loot = False

    def exit_game():
        keyboard.press('esc')
        keyboard.release('esc')

        pyautogui.moveTo(900, 470)
        pyautogui.click()

    def create_new_game(difficulty=2):
        pyautogui.moveTo(800, 960)
        pyautogui.click()

        if difficulty == 0:
            pyautogui.moveTo(930, 460)
        elif difficulty == 1:
            pyautogui.moveTo(930, 560)
        elif difficulty == 2:
            pyautogui.moveTo(930, 580)

        pyautogui.click()

    def insert_loot(self, runs_counter: RunCoutner):
        def close_top():
            top.destroy()
            root.destroy()
            self.inserting_item = False

        def add_item():
            runs_counter.add_loot(inpt.get())
            close_top()

        self.inserting_item = True
        root = ctk.CTk()
        top = ctk.CTkToplevel(root)
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
        root.withdraw()
        top.protocol('WM_DELETE_WINDOW', close_top)
        top.mainloop()

    def preview_loot(self, runs_counter: RunCoutner):
        def close_top():
            top.destroy()
            root.destroy()
            self.previewing_loot = False

        self.previewing_loot = True
        root = ctk.CTk()
        top = ctk.CTkToplevel(root)
        top.title('Previewing Looted Items')
        top.resizable(False, False)
        top.attributes('-topmost', True)

        loot_fr = ctk.CTkScrollableFrame(
            top, height=600, width=300,
            scrollbar_button_color='#2FA572',
            scrollbar_button_hover_color='#106A43'
        )
        loot_fr.pack(
            side=tk.LEFT, fill=tk.X, expand=tk.TRUE
        )

        for loot in runs_counter.loot:
            ctk.CTkLabel(
                loot_fr, text=loot, fg_color='transparent'
            ).pack(side=tk.TOP, fill=tk.X, expand=tk.TRUE)

        top.deiconify()
        root.withdraw()
        top.protocol('WM_DELETE_WINDOW', close_top)
        top.mainloop()
