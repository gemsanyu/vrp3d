from typing import Tuple, List

from item.item import Item

class Order:
    def __init__(self,
                 id:str,
                 customer_id:str,
                 item_list: List[Item],
                 coord:Tuple[float,float]):
        self.item_list: List[Item] = item_list
        self.coord = coord
        self.vehicle = None
        self.customer_id = customer_id
        self.id = id

    # def assign_to_vehicle(self, vehicle):
    #     self.vehicle = vehicle