from typing import Tuple

"""
    size: tuple (width, length, height) or (dx, dy, dz) or (span in x-axes, span in y-axes, span in z-axes)
    weigth: mass in gram
    position: (x,y,z) position in the Box, relative to left-bottom-deep-most corner of the item or (x=0,y=0,z=0)
"""
class Item:
    def __init__(self, 
                 size:Tuple[int,int,int], 
                 weight:int,
                 temp_class:int):
        size = sorted(size, reverse=True)
        self.original_size = size
        self.weight = weight
        self.temp_class = temp_class
        self.position = None
        self.volume = size[0]*size[1]*size[2]
        self.alternative_sizes = [
            (size[0], size[1], size[2]),
            (size[0], size[2], size[1]),
            (size[1], size[0], size[2]),
            (size[1], size[2], size[0]),
            (size[2], size[0], size[1]),
            (size[2], size[1], size[0]),
        ]
        self.alternative_sizes = sorted(self.alternative_sizes, key=lambda sz: (sz[2],sz[0],sz[1]))
        self.rotate_count = 0
    
    @property
    def size(self):
        return self.alternative_sizes[self.rotate_count%6]
    
    @property
    def face_area(self):
        size = self.size
        return size[0]*size[1]

    def __gt__(self, other):
        return self.volume < other.volume

    def __eq__(self, other):
        return self.volume == other.volume
    
    def rotate(self):
        self.rotate_count += 1