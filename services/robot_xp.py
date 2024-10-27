import math


class RobotXP:
    def __init__(self, xp: int):
        self.xp = xp
        self.level = self._get_level()
        self.level_bar = self._level_bar()
    
    def _get_level(self):
        if self.xp == 0: return 1
        return int(math.log(self.xp/10, 1.6)) + 1
    
    def _get_xp_for_level(self, level: int):
        return int(10 * (1.6 ** (level - 1)))
    
    def _level_bar(self):
        level_xp = self._get_xp_for_level(self.level)
        level_left = self.xp - level_xp
        gap = self._get_xp_for_level(self.level + 1) - level_xp
        m = (20*level_left/gap)
        main_bar = ["|" if i < m else "." for i in range(20)]
        return f"[{''.join(main_bar)}]"
    
    def __str__(self):
        return f"Level: {self.level}, XP: {self.xp}, Progress: {self.level_bar}"
