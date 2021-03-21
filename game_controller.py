import config
from base.render import Render
from view.title.scene import TitleScene
from view.game.scene import GameScene

"""
scene_index
-1: title scene
 0: game scene(Player vs Computer)
 1: game scene(Player vs Player)
 2: game scene(Computer vs Computer)
 3: help(未実装)
 4: exit
"""


class GameController():
    def __init__(self):
        self.scene_index = -1
        self.window = Render.init_cruses(
            config.WINDOW_HEIGHT, config.WINDOW_WIDTH, config.TIMEOUT)

    def run(self):
        while True:
            if self.scene_index == -1:
                title_scene = TitleScene(self.window, scene_number=-1)
                title_scene.run()
                self.scene_index = title_scene.selected_menu
            elif 0 <= self.scene_index <= 2:
                game_scene = GameScene(self.window)
                if self.scene_index == 0:
                    game_scene.regist_player_vs_computer()
                elif self.scene_index == 1:
                    game_scene.regist_player_vs_player()
                elif self.scene_index == 2:
                    game_scene.regist_computer_vs_computer()
                game_scene.run()
                self.scene_index = -1
            elif self.scene_index == 3:  # help
                pass
            elif self.scene_index == 4:
                break
            else:
                break

    def close_game(self):
        Render.close_cruses()
