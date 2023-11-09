from copy import deepcopy
from functools import partial, cmp_to_key
from math import ceil
from typing import List, Tuple

from item.item import Item
from item.box import Box


"""
    using binary search.
    input:  1. sorted box
            2. volume to fit
    output: index of the smallest fit box
"""
def find_smallest_fit_box(low:int, 
                         high:int, 
                         target_vol: int, 
                         box_list: List[Box]) -> int:
    if low > high:
        return -1
    mid = int((low+high)/2)
    if box_list[mid].volume >= target_vol:
        idx = find_smallest_fit_box(low, mid-1, target_vol, box_list)
        if idx == -1:
            return mid
    return find_smallest_fit_box(mid+1, high, target_vol, box_list)


def get_j(h:int, H:int, dt:float=7.83)->int:
    j = h*100/H/dt
    j = int(ceil(j))
    return j


"""
sort item first by their packing order (LIFO),
if same order, then:
this sorting simply sort non-increasingly
by area, then height as tiebreaker also non-increasing
"""
def cmp_item_ah(item1:Item, item2:Item):
    if item1.packing_order < item2.packing_order:
        return -1
    if item1.packing_order > item2.packing_order:
        return 1
    if item1.face_area < item2.face_area:
        return 1
    if item1.face_area > item2.face_area:
        return -1
    if item1.size[2]< item2.size[2]:
        return 1
    if item1.size[2]> item2.size[2]:
        return -1
    return 0

"""
sort item first by their packing order (LIFO),
if same order, then:
this sorting simply sort non-increasingly
by height, then area as tiebreaker also non-increasing
"""
def cmp_item_ha(item1:Item, item2:Item):
    if item1.packing_order < item2.packing_order:
        return -1
    if item1.packing_order > item2.packing_order:
        return 1
    if item1.size[2]< item2.size[2]:
        return 1
    if item1.size[2]> item2.size[2]:
        return -1
    if item1.volume < item2.volume:
        return 1
    if item1.volume > item2.volume:
        return -1
    return 0


"""
    sort item first by their packing order (LIFO),
    if same order, then:
    sorting the items based on clustered-height, then area
    dt is a parameter in the clustering method in
    the sorting 
"""
def cmp_item_cha(item1:Item, item2:Item, height:int, dt:float):
    if item1.packing_order < item2.packing_order:
        return -1
    if item1.packing_order > item2.packing_order:
        return 1
    j1 = get_j(item1.size[2], height, dt)
    j2 = get_j(item2.size[2], height, dt)
    if j1<j2:
        return 1
    if j1>j2:
        return -1
    if j1==j2:
        if item1.face_area < item2.face_area:
            return 1
        if item1.face_area > item2.face_area:
            return -1
    return 0

def sort_items_cha(box_list: List[Box], item_list: List[Item], dt:float) -> List[Item]:
    box_height = box_list[0].size[2]
    cmp_func = partial(cmp_item_cha, height=box_height, dt=dt)
    item_list = sorted(item_list, key=cmp_to_key(cmp_func))
    return item_list

# find ep that has minimum merit
def find_best_ep(box_list: List[Box], item:Item):
    box_i, ep_i  = -1, -1
    best_merit = 1000000
    for bi, box in enumerate(box_list):
        for ei, ep in enumerate(box.ep_list):
            if not box.is_insert_feasible(ep.pos, item):
                continue
            merit = ep.compute_merit(item.size)
            if merit< best_merit:
                best_merit = merit
                box_i, ep_i = bi, ei
    return box_i, ep_i

def find_first_ep(box_list: List[Box], item:Item):
    for bi, box in enumerate(box_list):
        for ei, ep in enumerate(box.ep_list):
            if not box.is_insert_feasible(ep.pos, item):
                continue
            return bi, ei
    return -1, -1
    



"""
    input: 1. List of available boxes
           2. List of items to pack
           3. Stop boxing threshold (zeta)
           after we find the smallest box that can
           fit the remaining items (if none exist, then
           get the biggest one), check if the remaining
           items at least can fit zeta% of the box's volume.
           Otherwise, it's wasting too much of the box space,
           then do not put them in a box.
           zeta=0 means box them regardless.
           zeta=1 means items must fit exactly or more than the box's vol.
           4. dt or delta is for the items sorting mechanism
"""
def pack_items_to_boxes(box_list: List[Box],
        item_list: List[Item],
        zeta: float=0.6,
        dt:float=7.83,
        is_best_fit:bool=True) -> Tuple[List[Box], List[Item]]:
    # Prepare
    box_list = sorted(box_list, key= lambda box: box.volume)
    for i, box in enumerate(box_list):
        box_list[i].reset()

    # duplicate items for each rotation
    dup_items: List[Item] = []
    for i, item in enumerate(item_list):
        item_list[i].rotate_count = 0
        for r in range(1,6):
            new_item = deepcopy(item)
            new_item.rotate_count = r
            dup_items += [new_item]
    item_list += dup_items
            
    #sort items
    if len(box_list) == 1:
        item_list = sort_items_cha(box_list, item_list, dt)
    else:
        item_list = sorted(item_list, key=cmp_to_key(cmp_item_ah))
    # item_list = sorted(item_list, key=cmp_to_key(cmp_item_ha))
    used_box:List[Box] = []
    unpacked_items:List[Item] = []
    remaining_volume  = sum([item.volume for item in item_list])
    
    # assign to box and pack
    while len(item_list) > 0:
        item = item_list[0]
        if is_best_fit:
            box_i, ep_i = find_best_ep(used_box, item)
        else:
            box_i, ep_i = find_first_ep(used_box, item)
        if box_i == -1:
            if len(box_list) == 0:
                unpacked_items += [item]
                del item_list[0]
                continue

            new_box_i = find_smallest_fit_box(0, len(box_list)-1, remaining_volume, box_list)
            new_box = box_list[new_box_i]
            # print(new_box.volume)
            left_over_volume = max(new_box.volume-remaining_volume,0)
            is_left_over_volume_above_threshold = left_over_volume >= new_box.volume*zeta
            if is_left_over_volume_above_threshold:
                unpacked_items += item_list
                return used_box, list(set(unpacked_items))
            
            used_box += [new_box]
            del box_list[new_box_i]
            box_i = len(used_box)-1
            ep_i = 0
        
        # succeeding in inserting
        used_box[box_i].insert(ep_i, item, is_using_rs=is_best_fit)
        # remove the duplicate items, in unpacked items
        for i in reversed(range(len(unpacked_items))):
            if unpacked_items[i].id == item.id:
                del unpacked_items[i]
        
        for i in reversed(range(len(item_list))):
            if item_list[i].id == item.id:
                del item_list[i]
        # used_box[box_i].visualize_packed_items()
    return used_box, list(set(unpacked_items))


def add_items_to_box(box:Box, item_list:List[Item])->bool:
    # duplicate items for each rotation
    dup_items: List[Item] = []
    for i, item in enumerate(item_list):
        item_list[i].rotate_count = 0
        for r in range(1,6):
            new_item = deepcopy(item)
            new_item.rotate_count = r
            dup_items += [new_item]
    item_list += dup_items
    item_list = sorted(item_list, key=cmp_to_key(cmp_item_ah))

    unpacked_items = []
    while len(item_list) > 0:
        item = item_list[0]
        box_i, ep_i = find_best_ep([box], item)
        if ep_i == -1:
            unpacked_items += [item]
            del item_list[0]
            continue

        # succeeding in inserting
        box.insert(ep_i, item, is_using_rs=False)
        # remove the duplicate items, in unpacked items
        for i in reversed(range(len(unpacked_items))):
            if unpacked_items[i].id == item.id:
                del unpacked_items[i]
        
        for i in reversed(range(len(item_list))):
            if item_list[i].id == item.id:
                del item_list[i]
    if len(unpacked_items)>0:
        return False
    return True


        
