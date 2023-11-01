from typing import Tuple

from order.item import Item

class Order:
    def __init__(self,
                 item:Item,
                 qty:int,
                 coord:Tuple[float,float]):
        self.item = item
        self.qty = qty
        self.coord = coord
        self.vehicle = None

    def assign_to_vehicle(self, vehicle):
        self.vehicle = vehicle