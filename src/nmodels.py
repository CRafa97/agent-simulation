from agents import *

class GoalDirect(Agent):
    def __init__(self):
        super().__init__()
        self.looked = None

    def see(self, env):
        pos = (self.x, self.y)
        dp = env.trash_pc()
        if not env.trash_pc() >= 0.4:
            if not self.carry and len(env.children):
                self.looked = near_entity(pos, env, ["c"])
            elif self.carry:
                self.looked = near_entity(pos, env, ["C"])
        self.looked = near_entity(pos, env, ["X"])

    @property
    def name(self):
        return "GoalDirect"

    def __str__(self):
        return "G" if not self.carry else "g"

class FirstTask(Agent):
    def __init__(self):
        super().__init__()
        self.looked = None

    def see(self, env):
        pos = (self.x, self.y)
        if self.carry:
            self.looked = near_entity(pos, env, ["C", "X"])
        else:
            self.looked = near_entity(pos, env, ["c", "X"])

    @property
    def name(self):
        return "FirstTask"

    def __str__(self):
        return "F" if not self.carry else "f"