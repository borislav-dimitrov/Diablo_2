import customtkinter as ctk
import tkinter as tk
import os

from utils import ItemCategory, THEME_COLORS, FONTS
from entities import Run, Item


class CreateItemWindow:
    def __init__(
        self, parent, run: Run, run_nr: str, color_normal: dict, color_hover: dict
    ) -> None:
        self._app_root = parent
        self._color_normal = color_normal
        self._color_hover = color_hover

        self._top = ctk.CTkToplevel(master=parent)
        self._top.title(f'Add a dropped item to run {run_nr}')
        self._top.geometry('350x400')
        self._top.after(
            200, lambda: self._top.iconbitmap(os.path.abspath(r'resources\icon.ico'))
        )
        self._top.resizable(False, False)
        self._top.protocol('WM_DELETE_WINDOW', self.close)

        self._item_type_opt_var = None
        self._descr_txt = None

        self._create_widgets()

        self.show()

    def _create_widgets(self) -> None:
        '''Create the widgets.'''
        WIDGET_PAD_X = 30
        WIDGET_PAD_Y = 0
        WIDGET_WIDTH = 130
        title_lbl = ctk.CTkLabel(
            self._top, text='Item properties',
            text_color=self._color_normal, font=FONTS['header_3']
        )
        title_lbl.pack(
            side=tk.TOP, padx=WIDGET_PAD_X, pady=WIDGET_PAD_Y
        )

        # region Category
        cat_fr = ctk.CTkFrame(self._top, fg_color='red')
        cat_fr.pack(
            side=tk.TOP, fill=tk.X, expand=tk.TRUE,
            padx=WIDGET_PAD_X, pady=WIDGET_PAD_Y
        )
        cat_lbl = ctk.CTkLabel(
            cat_fr, text='Category:',
            text_color=self._color_normal, font=FONTS['label']
        )
        cat_lbl.pack(side=tk.LEFT)

        self._item_type_opt_var = ctk.StringVar(value=ItemCategory.UNKNOWN)
        item_type_opt_values = [key for key in ItemCategory.__dict__.keys() if '__' not in key]
        item_type_opt = ctk.CTkOptionMenu(
            cat_fr, values=item_type_opt_values,
            variable=self._item_type_opt_var, width=WIDGET_WIDTH
        )
        item_type_opt.pack(side=tk.RIGHT, fill=tk.X, expand=tk.FALSE)
        # endregion

        # region Description
        descr_fr = ctk.CTkFrame(self._top, fg_color='green')
        descr_fr.pack(
            side=tk.TOP, fill=tk.X, expand=tk.TRUE,
            padx=WIDGET_PAD_X, pady=WIDGET_PAD_Y
        )
        descr_lbl = ctk.CTkLabel(
            descr_fr, text='Description:',
            text_color=self._color_normal, font=FONTS['label']
        )
        descr_lbl.pack(side=tk.LEFT)
        self._descr_txt = ctk.CTkEntry(
            descr_fr, placeholder_text='Input item description...',
            height=10, width=WIDGET_WIDTH
        )
        self._descr_txt.pack(side=tk.RIGHT, fill=tk.X, expand=tk.FALSE)
        # endregion

        # region Screenshot
        ss_fr = ctk.CTkFrame(self._top, fg_color='transparent')
        ss_fr.pack(
            side=tk.TOP, fill=tk.X, expand=tk.TRUE,
            padx=WIDGET_PAD_X, pady=WIDGET_PAD_Y
        )
        ss_lbl = ctk.CTkLabel(
            ss_fr, text='Screenshot:',
            text_color=self._color_normal, font=FONTS['label']
        )
        ss_lbl.pack(side=tk.LEFT, anchor='center')
        ss_controls_fr = ctk.CTkFrame(ss_fr, fg_color='transparent')
        ss_controls_fr.pack(side=tk.RIGHT, expand=tk.FALSE)
        ss_clipboard_btn = ctk.CTkButton(
            ss_controls_fr, text='Copy from clipboard',
            width=WIDGET_WIDTH, command=self._on_ss_from_clipboard
        )
        ss_clipboard_btn.pack(side=tk.TOP, expand=tk.FALSE, pady=5)
        ss_from_file_btn = ctk.CTkButton(
            ss_controls_fr, text='Add from file',
            width=WIDGET_WIDTH, command=self._on_ss_from_file
        )
        ss_from_file_btn.pack(side=tk.TOP, expand=tk.FALSE, pady=5)
        # endregion

        # region Controls
        controls_fr = ctk.CTkFrame(self._top, fg_color='transparent')
        controls_fr.pack(
            side=tk.BOTTOM, fill=tk.X, expand=tk.TRUE,
            padx=WIDGET_PAD_X, pady=WIDGET_PAD_Y
        )
        finish_btn = ctk.CTkButton(
            controls_fr, text='Finish', width=WIDGET_WIDTH, command=self._on_finish
        )
        finish_btn.pack(side=tk.LEFT, expand=tk.FALSE)
        cancel_btn = ctk.CTkButton(
            controls_fr, text='Cancel', width=WIDGET_WIDTH, command=self._on_cancel
        )
        cancel_btn.pack(side=tk.RIGHT, expand=tk.FALSE)
        # endregion

    def show(self) -> None:
        '''Show the create item window.'''
        self._app_root.iconify()
        self._top.focus()

    def close(self) -> None:
        '''Close the create item window.'''
        self._app_root.deiconify()
        self._top.destroy()

    def _on_ss_from_clipboard(self) -> None:
        '''Copy screenshot from clipboard.'''
        # TODO
        pass

    def _on_ss_from_file(self) -> None:
        '''Copy screenshot from file.'''
        # TODO
        pass

    def _on_finish(self) -> None:
        '''Finish Item creation and add it to the run.'''
        # TODO
        item_type = self._item_type_opt_var.get()
        description = self._descr_txt.get()
        print(item_type, description)

    def _on_cancel(self) -> None:
        '''Cancel adding item to run.'''
        self.close()
