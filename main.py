import sys
from curses import wrapper
from game_controller import GameController
from test import TestGameSceneRayout

# GameControllerにゲームの進行状況を持たせる
# GameControllerをSceneRendererに渡して，ゲームを描画する
# クラス間の依存関係を確認する


def main(stdscr):
    game_controller = GameController()
    game_controller.run()
    game_controller.close_game()


def test():
    test_game_scene = TestGameSceneRayout()
    test_game_scene.run()


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        wrapper(main)
    else:
        if args[1] == "--test":
            test()
        else:
            print("Argument is invalid.")
