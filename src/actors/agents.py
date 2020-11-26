from actors import *
from environment import Environment

class Agent:
    def __init__(self):
        self.carry = None

    def see(self, env):
        pass

    def action(self):
        pass

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

    def action(self, env):
        # in-place actions
        if self.info["A"].is_dirty:
            self.info["A"].dirty = False
            env.dirty -= 1
        elif isinstance(self.info["A"].entity, Cradle):
            self.info["A"].entity.child = self.carry
            self.carry = None
        else:
            step = 1 + bool(self.carry)

            while step:
                # first try get a child
                if not self.carry and self.info["c"]:
                    # compute step to child and get child
                    x, y = self.compute_next_move(self.info["c"])
                    env.move_agent(x, y)
                    if isinstance(env[x][y].entity, Child):
                        self.carry = env[x][y].entity
                        env.remove(self.carry)
                elif self.carry and (not self.info["X"] or (self.dist(self.info["C"]) < self.dist(self.info["X"]))):
                    # move to cradle
                    x, y = self.compute_next_move(self.info["C"])
                    env.move_agent(x, y)
                elif self.info["X"]:
                    # move to cradle
                    x, y = self.compute_next_move(self.info["X"])
                    env.move_agent(x, y)
                else:
                    pass

    def next(self, env):
        self.see(env)
        self.action(env)

    def dist(self, cell):
        x = cell.x
        y = cell.y
        return abs(x - self.x) + abs(y - self.y)

    def compute_next_move(self, cell, env):
        x = cell.x
        y = cell.y

        dx = (x - self.x) / abs(x - self.x)
        dy = (y - self.y) / abs(x - self.x)

        return x + dx, y + dy

        # if (str(env[x + dx][y + dy].entity) == "C" and env[x + dx][y + dy].entity.with_child) or \
        #     (str(env[x + dx][y + dy].entity) == "c" and self.carry) or \
        #         (str(env[x + dx][y + dy].entity) == "B"):
            
        #     if dx != 0 and dy != 0:
        #         return self.compute_next_move(env[x+dx][y]) or self.compute_next_move(env[x][y+dy]) 
        #     if dx == 0:
        #         return

class Proactive:
    pass

def near_actors(pos, env:Environment):    
    queue = [pos]
    d = { "C": None, "c": None, "X": None, "A": None, "B": None}
    while queue:
        x, y = queue.pop(0)
        # selector
        try:
            if str(env[x][y].entity) == "C" and env[x][y].entity.with_child:
                raise Exception() 
            d[str(env[x][y].entity)] = env[x][y] 
        except:
            pass
        queue += env.map_adj((x, y))
    return d