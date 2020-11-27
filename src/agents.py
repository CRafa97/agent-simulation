from entities import *
from utils import *
import numpy as np

class Agent:
    def __init__(self):
        self.carry = None

    def see(self, env):
        pass

    def action(self):
        pass

    def __str__(self):
        return "A"

class Reactive(Agent):
    def __init__(self):
        super().__init__()
        self.looked = None

    def see(self, env):
        pos = (self.x, self.y)
        self.looked = near_actor(pos, env, bool(self.carry))
        print(self.looked)

    def action(self, env):
        if env.env[self.x][self.y].is_dirty:
            env.env[self.x][self.y].dirty = False
            env.dirty -= 1
        elif isinstance(env.env[self.x][self.y].entity, Cradle) and self.carry:
            env.env[self.x][self.y].entity.child = self.carry
            self.carry = None
        
        step = 1 + bool(self.carry)

        while step:
            if str(self.looked) == "c":
                nx, ny = self.compute_next_move((self.looked.x, self.looked.y), env)
                env.move_agent(nx, ny)
                if str(env.env[self.x][self.y].entity) == "c":
                    self.carry = env.env[self.x][self.y].entity
                    env.remove_child(self.carry)
            else:
                nx, ny = self.compute_next_move((self.looked.x, self.looked.y), env, obs=["B", "c"])
                env.move_agent(nx, ny)
            step -= 1

    def next(self, env):
        self.see(env)
        self.action(env)

    def compute_next_move(self, pos, env, obs=["B"]):
        x, y = pos
        dx = np.sign(x - self.x)
        dy = np.sign(y - self.y)
        
        if str(env.env[x + dx][y + dy]) in obs:
           return rnd_choice(env.map_adj((x, y)), pred=lambda z: env.env[z[0]][z[1]].entity == None)

        return self.x + dx, self.y + dy

    def __str__(self):
        return "R"

class Proactive:
    pass

def near_actor(pos, env, child=False):    
    queue = [pos]
    mark = [ [ False for _ in range(len(env.env[0]))] for _ in range(len(env.env)) ]
    entity = None
    while queue:
        x, y = queue.pop(0)
        mark[x][y] = True
        # selector
        if (not child and str(env.env[x][y].entity) == "c") or \
            (str(env.env[x][y].entity) == "C" and not env.env[x][y].entity.with_child) or \
                env.env[x][y].is_dirty:

            entity = env.env[x][y]
            break

        for ax, ay in env.map_adj((x, y)):
            if not mark[ax][ay]:
                queue.append((ax, ay))
    return entity