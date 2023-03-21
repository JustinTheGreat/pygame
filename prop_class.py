from constants import *


class Prop:
    def __init__(self, **kwargs):
        self.pos_x = kwargs['pos_x']
        self.pos_y = kwargs['pos_y']
        self.sprite_ref = PROP_SPRITE_CODE + str(kwargs['type'])
        self.pos_z = 0
        self.parent = None

    def work(self):
        pass
