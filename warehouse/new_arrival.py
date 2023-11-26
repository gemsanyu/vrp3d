import numpy as np

from item.item import Item

class NewArrival(Item):
    def __init__(self, 
                 id: int, 
                 size: np.ndarray, 
                 name: str,
                 is_fast_moving: bool):
        super().__init__(id, size, name)
        self.is_fast_moving = is_fast_moving
        self.weight = 10