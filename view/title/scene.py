from base.scene import Scene
from view.title.render import TitleSceneRender


class TitleScene(Scene):

    def __init__(self, window, scene_number):
        self.selected_menu = 0
        self.render = TitleSceneRender(window)
        super().__init__(window, scene_number)

    def _render(self):
        self.render.render(self.selected_menu)

    def _key_up(self):
        if self.selected_menu > 0:
            self.selected_menu -= 1

    def _key_down(self):
        if self.selected_menu < 4:
            self.selected_menu += 1

    def _key_enter(self):
        self.scene_destination = self.selected_menu
