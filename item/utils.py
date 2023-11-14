from enum import Enum
from typing import Tuple

from numba.core.types.containers import UniTuple
from numba import int32, boolean
import numba as nb

from item.item import Item

class Temperature(Enum):
    COLD = 0
    CHILL_LOW = 1
    CHILL_HIGH = 2
    ROOM = 3

@nb.njit(boolean(int32,int32,int32,int32),cache=True)
def is_overlapping_1d(x1:int,dx1:int,x2:int,dx2:int):
    return x1 + dx1 >= x2 and x1 < x2 + dx2

@nb.njit(boolean(UniTuple(int32,3),UniTuple(int32,3),UniTuple(int32,3),UniTuple(int32,3)), cache=True)
def is_overlapping_3d(pos1:Tuple[int,int,int], 
                     size1:Tuple[int,int,int], 
                     pos2:Tuple[int,int,int], 
                     size2:Tuple[int,int,int]):
    return is_overlapping_1d(pos1[0], size1[0], pos2[0], size2[0]) and \
        is_overlapping_1d(pos1[1], size1[1], pos2[1], size2[1]) and \
        is_overlapping_1d(pos1[2], size1[2], pos2[2], size2[2])

@nb.njit(int32(int32,int32,int32,int32),cache=True)
def compute_overlap_1d(x1:int,dx1:int,x2:int,dx2:int):
    a = max(x1,x2)
    b = min(x1+dx1,x2+dx2)
    return max(b-a,0)

@nb.njit(int32(UniTuple(int32,3),UniTuple(int32,3),UniTuple(int32,3),UniTuple(int32,3)),cache=True)
def compute_supported_area(top_pos:Tuple[int,int,int], 
                           top_size:Tuple[int,int,int], 
                           bot_pos:Tuple[int,int,int], 
                           bot_size:Tuple[int,int,int]):
    is_bot_touch_top = bot_pos[2] + bot_size[2] == top_pos[2]
    if not is_bot_touch_top:
        return 0
    w = compute_overlap_1d(top_pos[0], top_size[0], bot_pos[0], bot_size[0])
    l = compute_overlap_1d(top_pos[1], top_size[1], bot_pos[1], bot_size[1])
    return w*l
    

def is_projection_valid_yx(item:Item, p_item:Item):
    return item.position[0] >= p_item.position[0] + p_item.size[0] and item.position[1] + item.size[1] < p_item.position[1] + p_item.size[1] and item.position[2] < p_item.position[2] + p_item.size[2]
    
def is_projection_valid_yz(item:Item, p_item:Item):
    return item.position[2] >= p_item.position[2] + p_item.size[2] and item.position[1] + item.size[1] < p_item.position[1] + p_item.size[1] and item.position[0] < p_item.position[0] + p_item.size[0]
    
def is_projection_valid_xy(item:Item, p_item:Item):
    return item.position[1] >= p_item.position[1] + p_item.size[1] and item.position[0] + item.size[0] < p_item.position[0] + p_item.size[0] and item.position[2] < p_item.position[2] + p_item.size[2]
    
def is_projection_valid_xz(item:Item, p_item:Item):
    return item.position[2] >= p_item.position[2] + p_item.size[2] and item.position[0] + item.size[0] < p_item.position[0] + p_item.size[0] and item.position[1] < p_item.position[1] + p_item.size[1]
    
def is_projection_valid_zx(item:Item, p_item:Item):
    return item.position[0] >= p_item.position[0] + p_item.size[0] and item.position[2] + item.size[2] < p_item.position[2] + p_item.size[2] and item.position[1] < p_item.position[1] + p_item.size[1]

def is_projection_valid_zy(item:Item, p_item:Item):
    return item.position[1] >= p_item.position[1] + p_item.size[1] and item.position[2] + item.size[2] < p_item.position[2] + p_item.size[2] and item.position[0] < p_item.position[0] + p_item.size[0]
    

