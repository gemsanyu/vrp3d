from typing import Tuple, Optional

from item.box import Box
# from vehicle.utils import TEMP..

WC_COMPUTATION_SHR = 0
WC_COMPUTATION_CUM = 1


class Vehicle:
    """
        temp_class: temperature class, 0-3, 
            lower temp_class can handle lower temperature
            so that 
    """
    def __init__(self,
                 vendor: str,
                 box: Box,
                 cost_per_km: int,
                 cost_per_kg: int,
                 temp_class: int,
                 max_duration: int,
                 ):
        self.vendor = vendor
        self.box = box 
        self.cost_per_km = cost_per_km 
        self.cost_per_kg = cost_per_kg
        self.temp_class = temp_class 
        self.max_duration = max_duration
        # self. = 

        self.tour = []
        self.packing_order = []
        self.arrival_time_list = []



def create_vehicle(vendor: str,
                    box_size: Tuple[int,int,int], 
                    box_max_weight:int,
                    cost_per_km: int,
                    cost_per_kg: int,
                    temp_class: int,
                    max_duration: int,) -> Vehicle:
    box = Box(box_size, box_max_weight)
    return  Vehicle(vendor, 
                      box, 
                      cost_per_km, 
                      cost_per_kg, 
                      temp_class, 
                      max_duration)
                      