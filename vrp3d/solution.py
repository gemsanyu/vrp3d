from typing import List, NamedTuple

class Solution(NamedTuple):
    tour_list: List[List[int]]
    packing_order_list: List[List[int]]
    packing_order_mode: int
    ep_sorting: int
    weight_cost: float
    distance_cost: float
    is_feasible: bool    

    