from random import randint, seed
from uuid import uuid1

from item.box import Box
from item.medicine import Medicine
from item.item import Item
from item.utils import Temperature
from packing.packing import pack_items_to_boxes


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
    box_list = []
    n_box = 10
    for i in range(n_box):
        box = Box(max_weight=1000, size=(randint(5,10), randint(5,10), randint(5,10)))
        box_list += [box]
    used_box, unpacked_items = pack_items_to_boxes(box_list, med_list, is_best_fit=False)
    for box in used_box:
        box.visualize_packed_items()
    print(len(used_box), len(unpacked_items))
    # print(len(unpacked_items))
    # print(med_list, box_list)
    # print(used_box[0].packed_items)



if __name__ == "__main__":
    seed(20)
    run()