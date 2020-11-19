import random as rnd

DIRS = [
    (0, 0), # represents stay position (first for ingore cases)
    #(-1,-1),
    (-1, 0),
    #(-1, 1),
    (0, -1),
    (0, 1),
    #(1, -1),
    (1, 0),
    #(1, 1),
]

def rnd_choice(l, pred=None):
    nl = l
    if pred:
        nl = list(filter(pred, l))
    elem = rnd.choice(nl)
    l.remove(elem)
    return elem
    