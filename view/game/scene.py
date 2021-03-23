from view.game.constant import (DEFAULT_PILE_SELECT_CURSOR_Y,
                                DEFAULT_PILE_SELECT_CURSOR_X,
                                PILE_COUNT, STONE_MAX,
                                PILE_NUMBER_LEFT_X, PILE_NUMBER_RIGHT_X,
                                SCALE_NUMBER_TOP_Y, SCALE_NUMBER_BOTTOM_Y)
import random
import numpy as np
from base.scene import Scene
from agent.computer_agent import ComputerAgent
from agent.player_agent import PlayerAgent
from view.game.render import GameSceneRender


class GameScene(Scene):
    def __init__(self, window, scene_number):
        self.round = 1
        self.start_player = 1
        self.turn_player_index = None
        self.turn_player = None
        self.is_game_active = True
        self.agents = []
        # self.fields = self._generate_field()
        self.fields = np.array([random.randrange(1, STONE_MAX + 1)
                                for _ in range(PILE_COUNT)])
        self.game_log = [("Game Start!!", "")]
        self.text = ""
        self.caution = ""
        self.pile_cursor_pos_x = DEFAULT_PILE_SELECT_CURSOR_X
        self.scale_cursor_pos_y = DEFAULT_PILE_SELECT_CURSOR_Y - 2
        self.render = GameSceneRender(window)
        super().__init__(window, scene_number)

    def run(self):
        while True:
            if self.is_game_active:
                # 変数の更新
                self.turn_player_index = (self.round + self.start_player) % 2
                self.turn_player = self.agents[self.turn_player_index]
                if isinstance(self.turn_player, PlayerAgent):
                    self._player_turn()
                elif isinstance(self.turn_player, ComputerAgent):
                    self._computer_turn()
            self._get_key_event()
            # 勝敗判定・処理
            self._judge_game_finished()
            if self.scene_destination != self.scene_number:
                break
            self._render()

    def regist_player_vs_player(self) -> None:
        self.agents.append(PlayerAgent())
        self.agents.append(PlayerAgent())

    def regist_player_vs_computer(self) -> None:
        self.agents.append(PlayerAgent())
        self.agents.append(ComputerAgent())

    def regist_computer_vs_computer(self) -> None:
        self.agents.append(ComputerAgent())
        self.agents.append(ComputerAgent())

    # def _generate_field(self) -> np.array:
    #     fields = np.zeros(PILE_COUNT)
    #     for i in range(PILE_COUNT):
    #         fields[i] = random.randrange(1, 21)
    #     return fields

    def _judge_game_finished(self):
        if self.is_game_active:
            if np.all(self.fields == 0):
                self.round -= 1
                if isinstance(self.turn_player, PlayerAgent):
                    self.game_log.append(("Player{} WIN the Game!!".format(
                        self.turn_player_index + 1),
                        "PRESS F1 Key. Back Main Menu"))
                elif isinstance(self.turn_player, ComputerAgent):
                    self.game_log.append(("Computer{} WIN the Game!!".format(
                        self.turn_player_index + 1),
                        "PRESS F1 Key. Back Main Menu"))
                self.is_game_active = False

    def _player_turn(self):
        if self.turn_player.scene == 0:
            self.text = "Please Select Pile."
        elif self.turn_player.scene == 1:
            self.text = "Please Select Stone."
        elif self.turn_player.scene == 2:
            self.agents[self.turn_player_index].scene = 0

            self.round += 1
        else:
            pass

    def _computer_turn(self):
        action = self.turn_player.action(self.fields)
        if self._is_correct_computer_action(self.fields, action):
            selected_pile = -1
            obtained_stone = -1
            for i in range(len(self.fields)):
                if self.fields[i] != action[i]:
                    selected_pile = i
                    obtained_stone = int(self.fields[i] - action[i])
                    break
            self.fields[selected_pile] -= obtained_stone

            self.game_log.append(
                ("Computer{}".format(self.turn_player_index + 1),
                 "Get {} Stone From No{} Pile.".format(
                 obtained_stone, selected_pile)
                 ))
            self.round += 1
        else:
            self.game_log.append(
                ("ERROR OCCURED IN", "COMPUTER ACTION VALIDATION")
            )

    def _is_correct_computer_action(self, before, after):
        change_flag = False
        for b, a in zip(before, after):
            if b != a:
                if change_flag:
                    return False
                else:
                    change_flag = True
        return change_flag

# カーソル移動関数

    def _key_up(self):
        if self.is_game_active:
            if isinstance(self.turn_player, PlayerAgent):
                if self.turn_player.scene == 1:
                    self._cursor_move_up()

    def _key_down(self):
        if self.is_game_active:
            if isinstance(self.turn_player, PlayerAgent):
                if self.turn_player.scene == 1:
                    self._cursor_move_down()

    def _key_left(self):
        if self.is_game_active:
            if isinstance(self.turn_player, PlayerAgent):
                if self.turn_player.scene == 0:
                    self._cursor_move_left()

    def _key_right(self):
        if self.is_game_active:
            if isinstance(self.turn_player, PlayerAgent):
                if self.turn_player.scene == 0:
                    self._cursor_move_right()

    def _key_enter(self):
        if self.is_game_active:
            if isinstance(self.turn_player, PlayerAgent):
                self.caution = ""
                if self.turn_player.scene == 0:
                    self._select_pile()
                elif self.turn_player.scene == 1:
                    self._select_stone_quantity()

    def _key_F1(self):
        if not self.is_game_active:
            self.scene_destination = -1

    def _cursor_move_left(self):
        if self.pile_cursor_pos_x > PILE_NUMBER_LEFT_X:
            self.pile_cursor_pos_x -= 2

    def _cursor_move_right(self):
        if self.pile_cursor_pos_x < PILE_NUMBER_RIGHT_X - 2:
            self.pile_cursor_pos_x += 2

    def _cursor_move_up(self):
        if self.scale_cursor_pos_y > SCALE_NUMBER_TOP_Y:
            self.scale_cursor_pos_y -= 1

    def _cursor_move_down(self):
        if self.scale_cursor_pos_y < SCALE_NUMBER_BOTTOM_Y - 1:
            self.scale_cursor_pos_y += 1

    def _select_pile(self):
        if PILE_NUMBER_LEFT_X <= self.pile_cursor_pos_x <= PILE_NUMBER_RIGHT_X:
            pile_index = (self.pile_cursor_pos_x - PILE_NUMBER_LEFT_X) // 2
            if self.fields[pile_index] > 0:
                self.agents[self.turn_player_index].selected_pile = pile_index
                self.agents[self.turn_player_index].scene = 1
            else:
                self.caution = "Please Select Pile that Remain the Stone."
        else:
            self.caution = "[Error]Select Pile Number is Out of Range"
            self.is_game_active = False

    def _select_stone_quantity(self):
        if SCALE_NUMBER_TOP_Y <= self.scale_cursor_pos_y <= SCALE_NUMBER_BOTTOM_Y:
            pile_index = self.turn_player.selected_pile
            stone_index = SCALE_NUMBER_BOTTOM_Y - self.scale_cursor_pos_y - 1
            if stone_index < self.fields[pile_index]:
                obtained_stone = self.fields[pile_index] - stone_index
                self.game_log.append(("Player{}".format(
                    self.turn_player_index + 1),
                    "Get {} Stone From No{} Pile.".format(
                    obtained_stone,
                    pile_index
                )))
                self.fields[pile_index] -= obtained_stone
                self.agents[self.turn_player_index].scene = 2
            else:
                self.caution = "Please Select Number You Can Get at Least 1"
        else:
            self.caution = "[Error]Select Count is Out of Range"

    def _render(self):
        self.render.render(self.turn_player, self.turn_player_index,
                           self.text, self.game_log,
                           self.pile_cursor_pos_x, self.scale_cursor_pos_y,
                           self.caution, self.fields)
