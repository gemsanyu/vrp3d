import enum
from typing import Tuple

from item.item import Item

"""
    size: tuple (width, length, height) or (dx, dy, dz) or (span in x-axes, span in y-axes, span in z-axes)
    weigth: mass in gram
    position: (x,y,z) position in the Box, relative to left-bottom-deep-most corner of the item or (x=0,y=0,z=0)
"""
class Medicine(Item):
    def __init__(self,
                 order_id:str,
                 customer_id:str,
                 product_id:str,
                 number:int,
                 uom: str, 
                 size:Tuple[int,int,int], 
                 weight:int,
                 temp_class:int):
        super(Medicine, self).__init__(size)
        self.weight = weight
        self.temp_class = temp_class
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.number = number
        self.uom = uom
        self.id = str(order_id)+"-"+str(customer_id)+\
            "-"+str(product_id)+"-"+str(number)




