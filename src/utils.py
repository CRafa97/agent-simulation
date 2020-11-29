import random as rnd

DIRS = [
    (0, 0), # represents stay position (first for ingore cases)
    (-1,-1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

def rnd_choice(l, pred=None, count=1):
    nl = l
    if pred:
        nl = list(filter(pred, l))
    elem = rnd.choice(nl)
    l.remove(elem)
    return elem
    
def rnd_choice_many(l, count):
    seq = []
    while count and l:
        seq.append(rnd_choice(l))
        count -= 1
    return seq
