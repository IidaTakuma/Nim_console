import sys
from game_controller import GameController

# GameControllerにゲームの進行状況を持たせる
# GameControllerをSceneRendererに渡して，ゲームを描画する
# クラス間の依存関係を確認する


def main():
    # ウィンドウの初期化
    game_controller = GameController()
    game_controller.run()


if __name__ == "__main__":
    main()
