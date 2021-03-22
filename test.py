from config import (WINDOW_HEIGHT, WINDOW_WIDTH)
from view.game.constant import (
    HALF_LINE_TOP_Y, HALF_LINE_BOTTOM_Y, HALF_LINE_X,
    TEXT_BOX_TOP_Y, TEXT_BOX_BOTTOM_Y, TEXT_BOX_LEFT_X, TEXT_BOX_RIGHT_X,
    FIELD_TOP_Y, FIELD_BOTTOM_Y, FIELD_LEFT_X, FIELD_RIGHT_X,
    PILE_LINE_Y, PILE_LINE_LEFT_X, PILE_LINE_RIGHT_X,
    PILE_NUMBER_Y, PILE_NUMBER_LEFT_X, PILE_NUMBER_RIGHT_X,
    SCALE_LINE_TOP_Y, SCALE_LINE_BOTTOM_Y, SCALE_LINE_X,
    SCALE_NUMBER_TOP_Y, SCALE_NUMBER_BOTTOM_Y, SCALE_NUMBER_X,
    MATRIX_TOP_Y, MATRIX_BOTTOM_Y, MATRIX_LEFT_X, MATRIX_RIGHT_X)


class TestGameSceneRayout:
    def __init__(self):
        pass

    def run(self):
        # 枠組みの座標
        assert 0 < HALF_LINE_X < WINDOW_WIDTH - 1
        assert 0 < HALF_LINE_TOP_Y < WINDOW_HEIGHT - 1
        assert 0 < HALF_LINE_BOTTOM_Y < WINDOW_HEIGHT - 1

        # テキストボックスの座標
        assert 0 < TEXT_BOX_TOP_Y < WINDOW_HEIGHT - 1
        assert 0 < TEXT_BOX_BOTTOM_Y < WINDOW_HEIGHT - 1
        assert 0 < TEXT_BOX_LEFT_X < WINDOW_WIDTH - 1
        assert 0 < TEXT_BOX_RIGHT_X < WINDOW_WIDTH - 1

        # 盤面の座標
        assert 0 < FIELD_TOP_Y < WINDOW_HEIGHT - 1
        assert 0 < FIELD_BOTTOM_Y < WINDOW_HEIGHT - 1
        assert 0 < FIELD_LEFT_X < WINDOW_WIDTH - 1
        assert 0 < FIELD_RIGHT_X < WINDOW_WIDTH - 1

        # 盤面 -> 下の線の座標
        assert 0 < PILE_LINE_Y < WINDOW_HEIGHT - 1
        assert 0 < PILE_LINE_LEFT_X < WINDOW_WIDTH - 1
        assert 0 < PILE_LINE_RIGHT_X < WINDOW_WIDTH - 1

        # 盤面 -> 下の番号の座標
        assert 0 < PILE_NUMBER_Y < WINDOW_HEIGHT - 1
        assert 0 < PILE_NUMBER_LEFT_X < WINDOW_WIDTH - 1
        assert 0 < PILE_NUMBER_RIGHT_X < WINDOW_WIDTH - 1

        # 盤面 -> 目盛りの線の座標
        assert 0 < SCALE_LINE_TOP_Y < WINDOW_HEIGHT - 1
        assert 0 < SCALE_LINE_BOTTOM_Y < WINDOW_HEIGHT - 1
        assert 0 < SCALE_LINE_X < WINDOW_WIDTH - 1

        # 盤面 -> 目盛りの番号の座標
        assert 0 < SCALE_NUMBER_TOP_Y < WINDOW_HEIGHT - 1
        assert 0 < SCALE_NUMBER_BOTTOM_Y < WINDOW_HEIGHT - 1
        assert 0 < SCALE_NUMBER_X < WINDOW_WIDTH - 1

        # 盤面 -> 石のmatrixの座標
        assert 0 < MATRIX_TOP_Y < WINDOW_HEIGHT - 1
        assert 0 < MATRIX_BOTTOM_Y < WINDOW_HEIGHT - 1
        assert 0 < MATRIX_LEFT_X < WINDOW_WIDTH - 1
        assert 0 < MATRIX_RIGHT_X < WINDOW_WIDTH - 1
