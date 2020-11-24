class Cell:
    def __init__(self, x, y, entity = None, agent = None, dirty = False):
        self.x = x
        self.y = y
        self.entity = entity
        self.agent = agent
        self.dirty = dirty

    def set_entity(self, entity):
        self.entity = entity
        self.entity.x = self.x
        self.entity.y = self.y

    def set_agent(self, agent):
        self.agent = agent
        self.agent.x = self.x
        self.agent.y = self.y

    def free_entity(self):
        self.entity = None

    def free_agent(self):
        self.agent = None

    @property
    def is_dirty(self):
        return self.dirty

    @property
    def is_empty(self):
        return self.entity == None and self.agent == None and not self.dirty

    def __str__(self):
        if self.entity:
            return str(self.entity)
        elif self.agent:
            return str(self.agent)
        elif self.dirty:
            return "X"
        else:
            return "-"