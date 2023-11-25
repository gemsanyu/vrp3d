from typing import Union

from item.box import Box
from item.cardboard import Cardboard

def get_a_box_copy(box:Union[Box,Cardboard]) -> Union[Box,Cardboard]:
    if isinstance(box, Box):
        return Box(box.id,
                   #box.size,
                   box.original_size, 
                   box.max_weight,
                   box.name,
                   box.support_alpha, 
                   box.temperature)
    
    return Cardboard(box.id, box.code, box.details,
                     box.original_size, box.max_weight,
                     box.support_alpha, box.temperature)