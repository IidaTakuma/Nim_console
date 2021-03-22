import sys
from curses import wrapper
from controller import Controller
from test import TestGameSceneRayout


def main(stdscr):
    controller = Controller()
    controller.run()
    controller.close_game()


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
