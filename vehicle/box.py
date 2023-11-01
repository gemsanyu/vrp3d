from collections import deque
from typing import List, Tuple

import matplotlib.pyplot as plt

from vehicle.item import Item
from vehicle.utils import is_overlapping_3d, compute_supported_area

# new_eps = [
#             (ep_yx),
#             (ep_yz),
#             (ep_xy),
#             (ep_xz),
#             (ep_zx),
#             (ep_zy)
#         ]
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
    


"""
    size: tuple (width, length, height) or (dx, dy, dz) or (span in x-axes, span in y-axes, span in z-axes)
    weigth: max weight of items inside it in gram

    ------
    extreme_points: possible insertion position, based on extreme-point based heuristic    
"""
class Box:
    def __init__(self, 
                 size: Tuple[int,int,int], 
                 max_weight:int,
                 support_alpha:float=0.51):
        self.size = size
        self.max_weight = max_weight
        self.volume = size[0]*size[1]*size[2]
        self.support_alpha = support_alpha
        self.packed_items: List[Item] = []
        self.extreme_points = [(0,0,0)]

        self.current_weight = 0
        self.current_volume = 0
    
    def pack_items_to_box(self, items: List[Item], is_order_strict=True) -> List[Item]:
        not_packed_items = []
        if not is_order_strict:
            items = sorted(items)
            # items = sorted(items, key=lambda item: (item.size[2], item.size[0], item.size[1]))
        items_deq = deque(items)
        while len(items_deq) > 0:
            # print(len(items_deq))
            item = items_deq.popleft()
            if not self.is_item_fit(item):
                not_packed_items += [item]
                continue
            self.extreme_points = sorted(self.extreme_points, key=lambda ep: (ep[2], ep[0], ep[1]))        
            is_inserted = False
            # print("------------------")
            # print(item.size)
            for ep in self.extreme_points:
                print(ep)
                if not self.is_insert_feasible(ep, item):
                    continue
                self.insert(ep, item)
                is_inserted = True
                self.visualize_packed_items()
                break

            if not is_inserted:
                if item.rotate_count == 5:
                    item.rotate_count = 0
                    not_packed_items += [item]
                else:
                    item.rotate()
                    items_deq.appendleft(item)

        return not_packed_items

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
        return self.current_volume + item.volume <= self.volume and \
            self.current_weight + item.weight <= self.max_weight
    
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

    def insert(self, position:Tuple[int,int,int], item:Item):
        self.current_volume += item.volume
        self.current_weight += item.weight
        item.position = position
        self.packed_items += [item]

        # now generate extreme points
        # 1. initial extreme points
        new_eps = [
            (position[0], position[1] + item.size[1], position[2]),
            (position[0], position[1] + item.size[1], position[2]),
            (position[0] + item.size[0], position[1], position[2]),
            (position[0] + item.size[0], position[1], position[2]),
            (position[0], position[1], position[2] + item.size[2]),
            (position[0], position[1], position[2] + item.size[2]),
        ]
        max_bound = [-1,-1,-1,-1,-1,-1]
        # 2. project these points 
        for p_item in self.packed_items:
            projx = p_item.position[0]+p_item.size[0]
            projy = p_item.position[1]+p_item.size[1]
            projz = p_item.position[2]+p_item.size[2]
            if is_projection_valid_yx(item, p_item) and projx > max_bound[0]:
                new_eps[0] = (projx, position[1] + item.size[1], position[2])
                max_bound[0] = projx
            if is_projection_valid_yz(item, p_item) and projz > max_bound[1]:
                new_eps[1] = (position[1], position[1] + item.size[1], projz)
                max_bound[1] = projz
            if is_projection_valid_xy(item, p_item) and projy > max_bound[2]:
                new_eps[2] = (position[0] + item.size[0], projy, position[2])
                max_bound[2] = projy
            if is_projection_valid_xz(item, p_item) and projz > max_bound[3]:
                new_eps[3] = (position[0] + item.size[0], position[1], projz)
                max_bound[3] = projz
            if is_projection_valid_zx(item, p_item) and projz > max_bound[4]:
                new_eps[3] = (projx, position[1], position[2] + item.size[2])
                max_bound[4] = projx
            if is_projection_valid_zy(item, p_item) and projy > max_bound[5]:
                new_eps[4] = (position[0], projy , position[2] + item.size[2])
                max_bound[5] = projy
        self.extreme_points += new_eps            
        # remove position from extreme points
        self.extreme_points.remove(position)

        # and remove duplicate extreme points
        self.extreme_points = list(set(self.extreme_points))

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