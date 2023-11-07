from random import randint
from uuid import uuid1

from item.box import Box
from item.medicine import Medicine
from item.item import Item
from item.utils import Temperature
from packing.bfd import bfd


def run():
    n_meds = 100
    med_list = []
    for i in range(n_meds):
        med = Medicine(order_id=str(uuid1()),
                       customer_id=str(uuid1()),
                       product_id=str(uuid1()),
                       number=0,
                       uom="box",
                       size=(randint(1,5), randint(1,5), randint(1,5)),
                       weight=randint(10,30),
                       temp_class=Temperature.ROOM)
        med_list += [med]
    box1 = Box(max_weight=1000, size=(10,10,10))
    box2 = Box(max_weight=1000, size=(5,4,5))
    box_list = [box1, box2]

    used_box, unpacked_items = bfd(box_list, med_list, dt=2)
    used_box[0].visualize_packed_items()
    used_box[1].visualize_packed_items()
    print(len(unpacked_items))
    # print(used_box[0].packed_items)



if __name__ == "__main__":
    run()