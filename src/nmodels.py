from agents import *

class GoalDirect(Agent):
    def __init__(self):
        super().__init__()
        self.looked = None

    def see(self, env):
        pos = (self.x, self.y)
        if not self.carry and len(env.children):
            self.looked = near_entity(pos, env, ["c"])
        else:
            self.looked = near_entity(pos, env, ["C", "X"])

    @property
    def name(self):
        return "Reactive"

    def __str__(self):
        return "R" if not self.carry else "r"