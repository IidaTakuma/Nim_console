from curses import (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER, KEY_F1)


class Scene:
    def __init__(self, window, scene_number):
        self.scene_number = scene_number
        self.scene_destination = scene_number
        self.window = window

    def run(self):
        while True:
            self._get_key_event()
            if self.scene_destination != self.scene_number:
                break
            self._render()

    def _render(self):
        pass

    def _get_key_event(self):
        event = self.window.getch()
        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER, KEY_F1]:
            if event == KEY_UP:
                self._key_up()
            elif event == KEY_DOWN:
                self._key_down()
            elif event == KEY_LEFT:
                self._key_left()
            elif event == KEY_RIGHT:
                self._key_right()
            elif event == KEY_ENTER:
                self._key_enter()
            elif event == KEY_F1:
                self._key_F1()
            else:
                return

    def _key_up(self):
        pass

    def _key_down(self):
        pass

    def _key_left(self):
        pass

    def _key_right(self):
        pass

    def _key_enter(self):
        pass

    def _key_F1(self):
        pass
