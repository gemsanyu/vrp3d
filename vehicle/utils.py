from typing import Tuple

TEMP_COLD = 0
TEMP_CHILL_LOW = 1
TEMP_CHILL_HIGH = 2
TEMP_ROOM = 3

def is_overlapping_1d(x1:int,dx1:int,x2:int,dx2:int):
    return x1 + dx1 >= x2 and x1 < x2 + dx2

def is_overlapping_3d(pos1:Tuple[int,int,int], 
                     size1:Tuple[int,int,int], 
                     pos2:Tuple[int,int,int], 
                     size2:Tuple[int,int,int]):
    return is_overlapping_1d(pos1[0], size1[0], pos2[0], size2[0]) and \
        is_overlapping_1d(pos1[1], size1[1], pos2[1], size2[1]) and \
        is_overlapping_1d(pos1[2], size1[2], pos2[2], size2[2])

def compute_overlap_1d(x1:int,dx1:int,x2:int,dx2:int):
    a = max(x1,x2)
    b = min(x1+dx1,x2+dx2)
    return max(b-a,0)

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
    