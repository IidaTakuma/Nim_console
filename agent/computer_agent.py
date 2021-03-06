import random
import numpy as np
from agent.agent import Agent


class ComputerAgent(Agent):

    def __init__(self):
        pass

    def action(self, fields):
        """
        func: 必勝条件を満たすなら必勝手を打つ，そうでないならランダムに動作する
        """
        fields_tmp = np.copy(fields)
        xor_sum = self.calc_xor_sum(fields_tmp)
        if xor_sum == 0:
            # 必勝手がない
            idx = -1
            while True:
                idx = random.randrange(0, len(fields_tmp))
                if fields_tmp[idx] != 0:
                    break

            cnt = random.randrange(1, fields_tmp[idx] + 1)
            fields_tmp[idx] -= cnt
        else:
            # 必勝手がある場合，全ての山で必勝手の可能性を試す
            for i, f in enumerate(fields_tmp):
                if f == 0:
                    continue

                xor_sum_tmp = xor_sum ^ int(f)
                remove = f - xor_sum_tmp
                if remove <= f and remove > 0:
                    fields_tmp[i] -= remove
                    break
        return fields_tmp

    def calc_xor_sum(self, fields):
        ret = 0
        for f in fields:
            ret ^= int(f)
        return ret
