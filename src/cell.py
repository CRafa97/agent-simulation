class Cell:
    def __init__(self, x, y, entity = None, dirty = False):
        self.x = x
        self.y = y
        self.entity = None
        self.dirty = dirty

    def set_entity(self, entity):
        self.entity = entity
        self.entity.x = self.x
        self.entity.y = self.y

    def free_entity(self):
        self.entity = None

    @property
    def is_dirty(self):
        return self.dirty

    @property
    def is_empty(self):
        return self.entity == None and not self.dirty

    def __str__(self):
        if self.entity:
            return str(self.entity)
        elif self.dirty:
            return "X"
        else:
            return "-"