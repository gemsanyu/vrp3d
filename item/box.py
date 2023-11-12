from copy import copy
from typing import List, Tuple, Optional
from uuid import uuid1

import matplotlib.pyplot as plt

from item.item import Item
from item.utils import is_overlapping_3d, compute_supported_area
from item.utils import is_projection_valid_xy, is_projection_valid_xz, is_projection_valid_yx, is_projection_valid_yz, is_projection_valid_zx, is_projection_valid_zy


"""
    extreme_points: possible insertion position, based on extreme-point based heuristic    
    we gonna use the Residual Space merit function here
    self.res is similar to size actually,
    the span to each axis, not overlapping with any item
    or, the distance in each axis to the closest item
"""
class EP:
    def __init__(self,
                 pos: Tuple[int,int,int],
                 res: Optional[Tuple[int,int,int]]=None) -> None:
        self.pos = pos
        self.res: Tuple[int, int, int] = res

    def update_res(self, item_pos:Tuple[int,int,int], item_size:Tuple[int,int,int]):
        if not is_overlapping_3d(self.pos, self.res, item_pos, item_size):
            return
        new_res = list(self.res)
        for i in range(3):
            if self.pos[i] < item_pos[i]:
                new_res[i] = min(self.res[i], item_pos[i]-self.pos[i])
        self.res = tuple(new_res)

    def compute_merit(self, item_size:Tuple[int,int,int]):
        return sum([self.res[i]-item_size[i] for i in range(3)])
    
    # these we need so that we can put EPs into a set, to remove
    # duplicates
    def __hash__(self) -> int:
        return hash(self.pos)
    
    def __eq__(self, other) -> bool:
        return self.pos == other.pos
        


class Box(Item):
    def __init__(self, 
                 size: Tuple[int,int,int], 
                 max_weight:int,
                 support_alpha:float=0.51,
                 temperature:int= 0):
        super(Box, self).__init__(size)
        self.id = str(uuid1())
        self.max_weight = max_weight
        self.support_alpha = support_alpha
        self.packed_items: List[Item] = []
        self.weight = 0
        self.filled_volume = 0
        self.temperature = temperature
        self.ep_list: List[EP] = []

    # reset to initial state
    # or to a given value (say a state of a solution)
    def reset(self,
              packed_items: Optional[List[Item]] = None,
              ep_list: Optional[List[EP]] = None):
        if packed_items is None:
            self.filled_volume = 0
            self.weight = 0
            self.packed_items = []
        else:
            self.packed_items = packed_items
            self.weight = sum([p_item.weight for p_item in packed_items])
            self.filled_volume = sum([p_item.volume for p_item in packed_items])
        self.init_extreme_points(ep_list)

    def init_extreme_points(self, ep_list: Optional[List[EP]] = None):
        if ep_list is None:
            self.ep_list = [EP((0,0,0),self.size)]
        else:
            self.ep_list = copy(ep_list)

    def update_ep_to_all_items(self, ep:EP):
        for item in self.packed_items:
            ep.update_res(item.position, item.size)

    """ FEASIBLE IFF
        1. placement does not cause item overflows edges
        2. it does not overlap other boxes
        3. alpha% of its bottom area are supported by other boxes or 
    """
    def is_insert_feasible(self, position:Tuple[int,int,int], item:Item) -> bool:
        is_overflow = position[0] + item.size[0] > self.size[0] or \
            position[1] + item.size[1] > self.size[1] or \
            position[2] + item.size[2] > self.size[2]
        if is_overflow:
            return False
        
        for p_item in self.packed_items:
            if is_overlapping_3d(position, item.size, p_item.position, p_item.size):
                return False

        is_item_at_bottom = position[2] == 0
        if is_item_at_bottom:
            return True
        total_supported_area = 0
        
        for p_item in self.packed_items:
            total_supported_area += compute_supported_area(position, 
                                                           item.size, 
                                                           p_item.position,
                                                           p_item.size)

        supported_ratio = total_supported_area/item.face_area
        return supported_ratio >= self.support_alpha
    
    def is_item_fit(self, item: Item):
        return self.filled_volume + item.volume <= self.volume and \
            self.weight + item.weight <= self.max_weight
    
    """
        new_eps = [
            (ep_yx),
            (ep_yz),
            (ep_xy),
            (ep_xz),
            (ep_zx),
            (ep_zy)
        ]
    """
    def insert(self, ep_i: int, item:Item, is_using_rs:bool):
        position = self.ep_list[ep_i].pos
        self.filled_volume += item.volume
        self.weight += item.weight
        item.position = position
        self.packed_items += [item]

        # now generate extreme points
        # 1. initial extreme points
        npos_list = [
            (position[0], position[1] + item.size[1], position[2]),
            (position[0], position[1] + item.size[1], position[2]),
            (position[0] + item.size[0], position[1], position[2]),
            (position[0] + item.size[0], position[1], position[2]),
            (position[0], position[1], position[2] + item.size[2]),
            (position[0], position[1], position[2] + item.size[2]),
        ]
        res_list = [tuple(self.size[j]-npos_list[i][j] for j in range(3)) for i in range(6)]
        new_eps = [EP(npos_list[i], res_list[i]) for i in range(6)]
        max_bound = [-1,-1,-1,-1,-1,-1]

        # 2. project these points 
        for p_item in self.packed_items:
            projx = p_item.position[0]+p_item.size[0]
            projy = p_item.position[1]+p_item.size[1]
            projz = p_item.position[2]+p_item.size[2]
            if is_projection_valid_yx(item, p_item) and projx > max_bound[0]:
                new_eps[0].pos = (projx, position[1] + item.size[1], position[2])
                max_bound[0] = projx
            if is_projection_valid_yz(item, p_item) and projz > max_bound[1]:
                new_eps[1].pos = (position[1], position[1] + item.size[1], projz)
                max_bound[1] = projz
            if is_projection_valid_xy(item, p_item) and projy > max_bound[2]:
                new_eps[2].pos = (position[0] + item.size[0], projy, position[2])
                max_bound[2] = projy
            if is_projection_valid_xz(item, p_item) and projz > max_bound[3]:
                new_eps[3].pos = (position[0] + item.size[0], position[1], projz)
                max_bound[3] = projz
            if is_projection_valid_zx(item, p_item) and projz > max_bound[4]:
                new_eps[3].pos = (projx, position[1], position[2] + item.size[2])
                max_bound[4] = projx
            if is_projection_valid_zy(item, p_item) and projy > max_bound[5]:
                new_eps[4].pos = (position[0], projy , position[2] + item.size[2])
                max_bound[5] = projy

        if is_using_rs:
            # update the new EPs residual space
            for i, ep in enumerate(new_eps):
                self.update_ep_to_all_items(new_eps[i])

            # update the old EPs residual space with
            # regard to the new item
            for i, ep in enumerate(self.ep_list):
                for item in self.packed_items:
                    self.ep_list[i].update_res(item.position, item.size)   

        # remove inserted position from extreme points
        del self.ep_list[ep_i]

        # add new EPs to EPlist
        self.ep_list += new_eps    

        # and remove duplicate extreme points
        self.ep_list = list(set(self.ep_list))
        if not is_using_rs:
            self.ep_list = sorted(self.ep_list, key=lambda ep: (ep.pos[2], ep.pos[1], ep.pos[0]))


    def plot_cube(self, ax, x, y, z, dx, dy, dz, color='red'):
        """ Auxiliary function to plot a cube. code taken somewhere from the web.  """
        xx = [x, x, x+dx, x+dx, x]
        yy = [y, y+dy, y+dy, y, y]
        kwargs = {'alpha': 1, 'color': color}
        ax.plot3D(xx, yy, [z]*5, **kwargs)
        ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
        ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
        ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
        ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
        ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)
    

    def visualize_packed_items(self):
        fig = plt.figure()
        axGlob = fig.add_subplot(projection='3d')
        # . plot scatola 
        self.plot_cube(axGlob,0, 0, 0, float(self.size[0]), float(self.size[1]), float(self.size[2]))
        # . plot intems in the box 
        colorList = ["black", "blue", "magenta", "orange"]
        counter = 0
        for item in self.packed_items:
            x,y,z = item.position
            color = colorList[counter % len(colorList)]
            self.plot_cube(axGlob, float(x), float(y), float(z), 
                     float(item.size[0]), float(item.size[1]), float(item.size[2]),
                     color=color)
            counter = counter + 1  
        plt.show()   


 # def pack_to_box(self, 
    #   items: List[Box], 
    #   is_order_strict=True, 
    #   ep_sorting_method=EP_SORT_ZYX,
    #   ) -> List[Item]:
    #     not_packed_items = []
    #     if not is_order_strict:
    #         items = sorted(items)
    #         # items = sorted(items, key=lambda item: (item.size[2], item.size[0], item.size[1]))
    #     items_deq = deque(items)
    #     while len(items_deq) > 0:
    #         # print(len(items_deq))
    #         item = items_deq.popleft()
    #         if not self.is_item_fit(item):
    #             not_packed_items += [item]
    #             continue

    #         if ep_sorting_method == EP_SORT_ZXY:
    #             self.ep_list = sorted(self.ep_list, key=lambda ep: (ep[2], ep[0], ep[1]))        
    #         elif ep_sorting_method == EP_SORT_ZYX:
    #             self.ep_list = sorted(self.ep_list, key=lambda ep: (ep[2], ep[1], ep[0]))       

    #         is_inserted = False
    #         # print("------------------")
    #         # print(item.size)
    #         for ep in self.ep_list:
    #             # print(ep)
    #             if not self.is_insert_feasible(ep, item):
    #                 continue
    #             self.insert(ep, item)
    #             is_inserted = True
    #             self.visualize_packed_items()
    #             break

    #         if not is_inserted:
    #             if item.rotate_count == 5:
    #                 item.rotate_count = 0
    #                 not_packed_items += [item]
    #             else:
    #                 item.rotate()
    #                 items_deq.appendleft(item)

    #     return not_packed_items