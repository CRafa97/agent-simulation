from actors import *
from environment import Environment

class Agent:
    def __init__(self):
        self.carry = None

    def see(self, env):
        pass

    def action(self):
        pass

    def dist(self, pos):
        x, y = pos
        return abs(x - self.x) + abs(y - self.y)

    def __str__(self):
        return "A"

class Reactive:
    def __init__(self):
        super().__init__()
        self.info = None

    def see(self, env):
        # get my current position and see env for near actors and trash
        pos = (self.x, self.y)
        self.info = near_actors(pos, env)

    def action(self):
        # first try get a child
        step = 1 + bool(self.carry)

        if not self.carry and self.info["c"]:
            # compute step to child
            pass
        elif self.carry:
            if not self.info["X"] or (self.dist(self.info["C"]) < self.dist(self.info["X"])):
                # move to cradle
            else:
                # move to trash

class Proactive:
    pass

def near_actors(pos, env:Environment):    
    queue = [pos]
    d = { "C": None, "c": None, "X": None }
    while queue:
        x, y = queue.pop(0)
        # selector
        try:
            if str(env[x][y].entity) == "C" and env[x][y].entity.with_child:
                raise Exception() 
            d[str(env[x][y].entity)] = (x, y)
        except KeyError:
            pass
        queue += env.map_adj((x, y))
    return d