import pyautogui
import keyboard


class HotKeys:
    def __init__(self) -> None:
        self.inserting_item = False
        self.previewing_loot = False

    def exit_game(self):
        keyboard.press('esc')
        keyboard.release('esc')

        pyautogui.moveTo(900, 470)
        pyautogui.click()

    def create_new_game(self, difficulty=2):
        pyautogui.moveTo(800, 960)
        pyautogui.click()

        if difficulty == 0:
            keyboard.press('r')
            keyboard.release('r')
        elif difficulty == 1:
            keyboard.press('n')
            keyboard.release('n')
        elif difficulty == 2:
            keyboard.press('h')
            keyboard.release('h')
