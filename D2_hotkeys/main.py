from threading import Thread
import keyboard
from hotkeys import HotKeys
from run_counter import RunCoutner
from views import Views


class Difficulties:
    NORMAL = 0
    NIGHTMARE = 1
    HELL = 2


class RunSettings:
    DEFAULT = {
        'file': 'default.json',
        'difficulty': Difficulties.HELL
    }
    MEPHISTO_NM = {
        'file': 'mephisto_nm.json',
        'difficulty': Difficulties.NIGHTMARE
    }
    ANDARIEL_NM = {
        'file': 'andariel_nm.json',
        'difficulty': Difficulties.NIGHTMARE
    }
    ANDARIEL_HELL = {
        'file': 'andariel_hell.json',
        'difficulty': Difficulties.HELL
    }


SELECTED_RUN = RunSettings.ANDARIEL_HELL
HOTKEYS = HotKeys()
RUN_COUNTER = RunCoutner(SELECTED_RUN['file'])
VIEWS = Views(RUN_COUNTER)


def on_key_press(event):
    if event.name == 'f5':
        HOTKEYS.exit_game()
    elif event.name == 'f6':
        HOTKEYS.create_new_game(difficulty=SELECTED_RUN['difficulty'])
        RUN_COUNTER.add_run()
        VIEWS.update_runs()
    elif event.name == 'f7':
        VIEWS.insert_loot()
    elif event.name == 'f8':
        VIEWS.preview_loot()
    elif event.name == 'f9':
        VIEWS.toggle_overlay()
    elif event.name == 'f12':
        VIEWS.close_all_views()


def main_func():
    RUN_COUNTER.load()
    keyboard.on_press(on_key_press)
    VIEWS.run_main_view()
    RUN_COUNTER.save()


if __name__ == '__main__':
    main_func()
