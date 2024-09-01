import keyboard
from hotkeys import HotKeys
from run_counter import RunCoutner


hotkeys = HotKeys()
run_counter = RunCoutner()


def on_key_press(event):
    if event.name == 'f5':
        hotkeys.exit_game()
    elif event.name == 'f6':
        hotkeys.create_new_game()
    elif event.name == 'f7':
        hotkeys.insert_loot(run_counter)
    elif event.name == 'f8':
        hotkeys.preview_loot(run_counter)


def main_func():
    run_counter.load()
    keyboard.on_press(on_key_press)

    keyboard.wait('f12')
    run_counter.save()


if __name__ == '__main__':
    main_func()
