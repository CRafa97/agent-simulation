class Child:
    def __init__(self):
        pass

    def __str__(self):
        return "c"    

class Cradle:
    def __init__(self):
        self.child = None

    @property
    def with_child(self):
        return self.child != None

    def __str__(self):
        return "C"

class Block:
    def __init__(self):
        pass

    def __str__(self):
        return "B"