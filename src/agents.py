from entities import *
from utils import *
import numpy as np

class Agent:
    def __init__(self):
        self.carry = None

    def see(self, env):
        pass

    def action(self, env):
        if env.env[self.x][self.y].is_dirty:
            env.env[self.x][self.y].dirty = False
            env.dirty -= 1
        elif isinstance(env.env[self.x][self.y].entity, Cradle) and self.carry:
            env.env[self.x][self.y].entity.child = self.carry
            self.carry = None
        else:
            if self.looked is None:
                return

            step = 1 + bool(self.carry)

            while step:
                if str(self.looked) == "c":
                    nx, ny = self.compute_next_move((self.looked.x, self.looked.y), env)
                    env.move_agent(nx, ny)
                    if str(env.env[self.x][self.y].entity) == "c":
                        self.carry = env.env[self.x][self.y].entity
                        env.env[self.x][self.y].entity = None
                        env.remove_child(self.carry)
                else:
                    nx, ny = self.compute_next_move((self.looked.x, self.looked.y), env, obs=["B", "C", "c"])
                    env.move_agent(nx, ny)
                step -= 1

    def next(self, env):
        self.see(env)
        self.action(env)

    def compute_next_move(self, pos, env, obs=["B", "C"]):
        x, y = pos
        dx = np.sign(x - self.x)
        dy = np.sign(y - self.y)
        
        if str(env.env[self.x + dx][self.y + dy]) in obs:
            if str(env.env[self.x + dx][self.y + dy]) == "C" and not env.env[self.x + dx][self.y + dy].entity.with_child:
                pass
            else:
                try: # cannot choice a pos, bot blocked
                    return rnd_choice(env.map_adj((self.x, self.y)), pred=lambda z: env.env[z[0]][z[1]].entity == None)
                except:
                    # cannot choice a pos, bot blocked
                    return self.x, self.y

        return self.x + dx, self.y + dy

    def __str__(self):
        return "A"

class Reactive(Agent):
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

class Proactive(Agent):
    def __init__(self):
        super().__init__()
        self.looked = None

    def see(self, env):
        pos = (self.x, self.y)
        dp = env.trash_pc()
        if not self.carry and len(env.children):
            self.looked = near_entity(pos, env, ["c"])
        elif self.carry:
            self.looked = near_entity(pos, env, ["C"])
        else:
            self.looked = near_entity(pos, env, ["X"])

    @property
    def name(self):
        return "Proactive"

    def __str__(self):
        return "P" if not self.carry else "p"

def near_entity(pos, env, search):    
    queue = [pos]
    mark = [ [ False for _ in range(len(env.env[0]))] for _ in range(len(env.env)) ]
    entity = None
    while queue:
        x, y = queue.pop(0)
        mark[x][y] = True
        if str(env.env[x][y]) in search:
            if str(env.env[x][y]) == "C" and env.env[x][y].entity.with_child:
                pass     
            else:
                entity = env.env[x][y]
                break
        for ax, ay in env.map_adj((x, y)):
            if not mark[ax][ay]:
                queue.append((ax, ay))
    return entity