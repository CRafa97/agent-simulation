from cell import Cell
from entities import *
from agents import *
from utils import *
import random as rnd

class Environment:
    def __init__(self, N, M, t, dp, bp, childn, agent):
        self.N = N
        self.M = M
        self.t = t
        self.env = []
        self.agent = agent
        self.cradles = [ Cradle() for _ in range(childn) ]
        self.children = [ Child() for _ in range(childn) ]
        self.blocking = [ Block() for _  in range(int( (bp*N*M)/100 )) ]
        self.dirty = int( (dp*N*M)/100 )

        self.remake()

    def is_clean(self):
        return self.dirty == 0 and all(c.with_child for c in self.cradles)

    def trash_pc(self):
        return (self.dirty / ((self.N * self.M) - len(self.cradles) - len(self.children) - len(self.blocking) - 1)) 

    def remake(self):
        self.env = [ [ Cell(i, j) for j in range(self.M) ] for i in range(self.N) ] # clean env
        cells = [ (r, c) for r in range(self.N) for c in range(self.M) ]
        rnd.shuffle(cells)

        # set cradles
        x, y = rnd_choice(cells)
        for cradle in self.cradles: 
            self.env[x][y].set_entity(cradle)
            try:
                x, y = rnd_choice(cells, pred= lambda z: z in self.map_adj((x, y)))
            except:
                self.remake() # try again set cradles
                return

        # set agent in same position
        x, y = rnd_choice(cells)
        self.env[x][y].set_agent(self.agent)

        # set children and blocking
        for entity in self.children + self.blocking:
            x, y = rnd_choice(cells)
            self.env[x][y].set_entity(entity)

        # set dirty
        for _ in range(self.dirty):
            x, y = rnd_choice(cells)
            self.env[x][y].dirty = True

    def next(self):
        """ Change the env to next state """
       
        def can_move_block(x, y, dir):
            bx, by = x + dir[0], y + dir[1]
            if not self.is_inside(bx, by):
                return False
            
            if self.env[bx][by].is_empty or (isinstance(self.env[bx][by].entity, Block) and can_move_block(bx, by, dir)):
                blk = self.env[x][y].entity
                self.env[x][y].free_entity()
                self.env[bx][by].set_entity(blk)
                return True
            else:
                return False

        squares = []

        for child in self.children:
            x = child.x
            y = child.y

            # count new dirty zones using children
            adjs = self.square(x, y)
            pchild = list(filter(lambda z: isinstance(self.env[z[0]][z[1]].entity, Child), adjs))
            empties = list(filter(lambda z: self.env[z[0]][z[1]].is_empty, adjs))
            count = len(pchild)
            new_trash = rnd.randint(0, (count * (count == 1) + 3 * (count == 2) + 6*(count >= 3)))
            
            squares.append((empties, new_trash))

            nx, ny = rnd.choice(self.map_adj((x, y), not_stay=False))

            if x == nx and y == ny:
                continue

            if self.env[nx][ny].is_empty or (isinstance(self.env[nx][ny].entity, Block) and can_move_block(nx, ny, (nx - x, ny - y))):
                self.env[x][y].free_entity()
                self.env[nx][ny].set_entity(child)
            else:
                pass

        # put trash in env
        for pos, cnt in squares:
            for tx, ty in rnd_choice_many(pos, cnt):
                if self.env[tx][ty].is_empty: 
                    self.env[tx][ty].dirty = True
                    self.dirty += 1

    def insert_agent(self, x, y, agent):
        self.env[x][y].set_agent(agent)
        self.agent = self.env[x][y].agent

    def move_agent(self, x, y):
        self.env[self.agent.x][self.agent.y].free_agent()
        self.insert_agent(x, y, self.agent)

    def remove_child(self, child):
        self.children.remove(child)

    def square(self, x, y):
        adjs = []
        for d in SQUARE:
            nx = x + d[0]
            ny = y + d[1]

            if self.is_inside(nx, ny):
                adjs.append((nx, ny))

        return adjs

    def map_adj(self, pos, pred=None, not_stay=True):
        adjs = []
        for d in DIRS[not_stay:]:
            x = pos[0] + d[0]
            y = pos[1] + d[1]
            if self.is_inside(x, y):
                adjs.append((x, y))
        if pred:
            adjs = list(filter(pred, adjs))
        return adjs

    def is_inside(self, x, y):
        return 0 <= x < self.N and 0 <= y < self.M 

    def __str__(self):
        return '\n'.join(' '.join(str(self.env[i][j]) for j in range(self.M)) for i in range(self.N))