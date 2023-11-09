from random import randint, seed
from uuid import uuid1

from item.box import Box
from item.medicine import Medicine
from item.item import Item
from item.utils import Temperature
from packing.packing import pack_items_to_boxes
from data.GenerateData import ProblemGenerator

def run():
    # tes initialize VRP3D
    n_vec = 5
    n_ord = 100
    max_item_type_qty = 10
    max_order_item_qty = 30 
    ProblemGenerator.initialize()
    vrps = ProblemGenerator.generate_problem(n_vec, n_ord, max_item_type_qty, max_order_item_qty)



    # tes visualisasi bin packing
    # med dipack ke dus, dus dipack ke box vehicle
    n_meds = 100
    '''
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
    '''
    med_list = ProblemGenerator.generate_random_medicines_nocus(n_meds)
    n_box = 10

    dus_list = ProblemGenerator.get_random_duses(1000)
    vec_list = ProblemGenerator.generate_random_vehicles(n_box)
    vec_box_list = [vec_list[i].box for i in range(len(vec_list))]
    print("len duses : ", len(dus_list))
    print("len boxes : ", len(vec_box_list))


    '''
    box_list = []
    for i in range(n_box):
        box = Box(max_weight=1000, size=(randint(5,10), randint(5,10), randint(5,10)))
        box_list += [box]
    used_box, unpacked_items = pack_items_to_boxes(box_list, med_list, is_best_fit=False)
    '''
    used_dus, unpacked_items = pack_items_to_boxes(dus_list, med_list, is_best_fit=False, zeta=1)
    print("len used duses : ", len(used_dus))
    used_box, unpacked_duses = pack_items_to_boxes(vec_box_list, used_dus, is_best_fit=False, zeta=1)
    print("len used duses : ", len(used_dus))
    print("len used boxes : ", len(used_box))
    for dus in used_dus:
        dus.visualize_packed_items()
    for box in used_box:
        box.visualize_packed_items()
    print(len(used_box), len(unpacked_items))


    # print(len(unpacked_items))
    # print(med_list, box_list)
    # print(used_box[0].packed_items)



if __name__ == "__main__":
    seed(20)
    run()