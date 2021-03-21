import sys
from game_controller import GameController
from view.game.scene import TestGameScene

# GameControllerにゲームの進行状況を持たせる
# GameControllerをSceneRendererに渡して，ゲームを描画する
# クラス間の依存関係を確認する


def main():
    game_controller = GameController()
    game_controller.run()
    game_controller.close_game()


def test():
    test_game_scene = TestGameScene()
    test_game_scene.run()


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        main()
    else:
        if args[1] == "--test":
            test()
        else:
            print("Argument is invalid.")
