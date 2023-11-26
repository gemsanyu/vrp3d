from typing import List

import numpy as np
import matplotlib.pyplot as plt

from warehouse.rack import Rack

class Room:
    def __init__(self, 
                 rack_list: list[Rack],
                 size: np.ndarray = np.asanyarray([1000,1000,3000], dtype=np.int32)
                 ) -> None:
        self.rack_list = rack_list
        self.size = size
        self.door_size = np.asanyarray([10, 300, 10], dtype=np.int32)
        self.door_position = np.asanyarray([1000, 350, 0], dtype=np.int32)
        for i, rack in enumerate(rack_list):
            for j, pallet in enumerate(rack.pallet_list):
                self.rack_list[i].pallet_list[j].compute_distance_to_door(rack.position,self.door_position, self.door_size)

    def plot_cube(self, ax, x, y, z, dx, dy, dz, color='red', text_annot:str=""):
        """ Auxiliary function to plot a cube. code taken somewhere from the web.  """
        xx = [x, x, x+dx, x+dx, x]
        yy = [y, y+dy, y+dy, y, y]
        kwargs = {'alpha': 1, 'color': color}
        artists = []
        artists+= ax.plot3D(xx, yy, [z]*5, **kwargs)
        artists+= ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
        artists+= ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
        artists+= ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
        artists+= ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
        artists+= ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)
        # if text_annot!="":
        #     artists+= [ax.text(x+dx/2,y,z+dz/2,text_annot,None,fontweight=1000)]
        return artists
    
    def visualize(self):
        fig = plt.figure()
        axGlob = fig.add_subplot(projection='3d')
        # plot floor
        self.plot_cube(axGlob, 0, 0, -1, float(self.size[0]), float(self.size[1]), 1, color="white")
        # plot door
        door_pos = self.door_position
        door_size = self.door_size
        self.plot_cube(axGlob, door_pos[0], door_pos[1], door_pos[2], door_size[0], door_size[1], 5, color="grey")
        
        # plot racks
        for ri, rack in enumerate(self.rack_list):
            rpos = rack.position
            for pi, pallet in enumerate(rack.pallet_list):
                psize = pallet.size
                ppos = pallet.position
                self.plot_cube(axGlob, rpos[0]+ppos[0], rpos[1]+ppos[1], rpos[2]+ppos[2], psize[0], psize[1], 0.5, color="brown")
        
                # . plot intems in the box 
                # colorList = ["black", "blue", "magenta", "orange"]
                counter = 0
                for item in pallet.packed_items:
                    print(item.position,"----------")
                    x,y,z = item.position + rpos + ppos
                    # print(item.position, rpos, ppos, x,y,z)
                    # color = colorList[counter % len(colorList)]
                    color = "blue" if item.is_fast_moving else "orange"
                    self.plot_cube(axGlob, float(x), float(y), float(z), 
                            float(item.size[0]), float(item.size[1]), float(item.size[2]),
                            color=color,text_annot=str(item.insertion_order))
                    counter = counter + 1  
        plt.show() 