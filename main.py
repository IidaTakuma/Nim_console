import sys

from game_controller import GameController

DEBUG = False


def main():
    game_controller = GameController()
    game_controller.process()


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "debug" or args[1] == "--d":
            DEBUG = True
    main()
