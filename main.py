from random import randint, seed
from typing import List
from uuid import uuid1

from item.box import Box
from item.medicine import Medicine
from item.item import Item
from item.utils import Temperature
from order.order import Order
from packing.packing import pack_items_to_boxes
from vehicle.vehicle import Vehicle, create_vehicle
from vns.greedy_init import greedy_initialization
from vrp3d.solution import Solution
from vrp3d.vrp3d import VRP3D
from data.GenerateData import ProblemGenerator



lat_lon_list = [
                [41.39753660, 2.12356330],
                [41.40052560, 2.11713440],
                [41.39406020, 2.19094860],
                [41.42137720, 2.08627070],
                [41.42227070, 2.13323310],
                [41.43640110, 2.18893560],
                [41.39797200, 2.17343800],
                [41.43220000, 2.16124700],
                [41.41009850, 2.18822350],
                [41.43215450, 2.18508420],
                [41.39825330, 2.17687800],
                [41.43531630, 2.08933260],
                [41.39491220, 2.13269920],
                [41.44181900, 2.17304600],
                [41.39691210, 2.12195190],
                [41.40289610, 2.10700030],
                [41.42202810, 2.17641570],
                [41.38104350, 2.18867720],
                [41.39289310, 2.15261720],
                [41.44252360, 2.17430660],
                [41.38859690, 2.18120880],
                [41.39809180, 2.17319740],
                [41.42876960, 2.09558440],
                [41.43418680, 2.16529700],
                [41.42457780, 2.15607310],
                [41.38892640, 2.17960100],
                [41.41895940, 2.14909610],
                [41.41927790, 2.14900990],
                [41.38534280, 2.17170190],
                [41.39560560, 2.17296570],
                [41.42487430, 2.15596920],
                [41.39713230, 2.12343660],
                [41.44193550, 2.19008920],
                [41.43460950, 2.15629080],
                [41.43342200, 2.18441240],
                [41.39843170, 2.17893870],
                [41.42938860, 2.17646510],
                [41.42690600, 2.18465540],
                [41.38785930, 2.17799060],
                [41.43074650, 2.16251410],
                [41.38672140, 2.17353810],
                [41.41695530, 2.21603250],
                [41.43314540, 2.18911240],
                [41.36250330, 2.07296610],
                [41.38226980, 2.13802490],
                [41.37961100, 2.08964820],
                [41.39716020, 2.19588250],
                [41.42256580, 2.09726060],
                [41.41273970, 2.18130290],
                [41.38963490, 2.10462520],
                [41.44984240, 2.20782730],
                [41.39747430, 2.12799110],
                [41.41266620, 2.16020560],
                [41.39002880, 2.11717190],
                [41.44289120, 2.21485120],
                [41.44130830, 2.20664850],
                [41.42233050, 2.18189410],
                [41.42474170, 2.17131170],
                [41.37019390, 2.05809080],
                [41.43119840, 2.18743590],
                [41.39245750, 2.16795150],
                [41.39407070, 2.18067200],
                [41.40364660, 2.19934050],
                [41.40768350, 2.17528990],
                [41.39244310, 2.10492030],
                [41.35605100, 2.06936610],
                [41.44128310, 2.20095760],
                [41.39163460, 2.18771500],
                [41.40178920, 2.20672040],
                [41.32571630, 2.09067340],
                [41.38414740, 2.05186090],
                [41.40577680, 2.15391600],
                [41.40332330, 2.15611370],
                [41.39674930, 2.11219220],
                [41.36556140, 2.05301940],
                [41.43799330, 2.17923500],
                [41.42301310, 2.15237270],
                [41.39629540, 2.15095100],
                [41.36498840, 2.12658370],
                [41.45021920, 2.07829240],
                [41.43189850, 2.16301530],
                [41.40261880, 2.17579990],
                [41.43224650, 2.16349840],
                [41.38210560, 2.17609720],
                [41.40367350, 2.16212660],
                [41.35864420, 2.10061820],
                [41.38535170, 2.15536850],
                [41.44360710, 2.18076910],
                [41.36228790, 2.10872500],
                [41.38442060, 2.14052840],
                [41.45231470, 2.22570450],
                [41.40009880, 2.16306440],
                [41.37254470, 2.12285750],
                [41.42443860, 2.19060250],
                [41.32342770, 2.08813950],
                [41.44988800, 2.23682230],
                [41.43955720, 2.21901660],
                [41.39414000, 2.13906990],
                [41.42861460, 2.23363630],
                [41.39860540, 2.16167630],
                [41.37970190, 2.16988380],
            ]

def generate_orders(n_order, max_n_med) -> List[Order]:
    order_list = []
    for i in range(n_order):
        order_id = str(uuid1())
        customer_id = str(uuid1())
        coord = tuple(lat_lon_list[randint(0,len(lat_lon_list)-1)])

        n_med = randint(4,max_n_med)
        med_list = []
        for j in range(n_med):
            product_id = str(uuid1())
            med_size = (randint(1,5), randint(1,5), randint(1,5))
            med = Medicine(order_id, customer_id, product_id, number=0,
                           uom='box', size=med_size, weight=randint(10,30),
                           temp_class=Temperature.COLD)
            med_list += [med]
        order = Order(order_id, customer_id, med_list, coord)
        order_list += [order]
    return order_list

def generate_cardboard_boxes():
    cbox_list = []
    n_box = 10
    for i in range(n_box):
        box = Box(max_weight=1000, size=(randint(5,10), randint(5,10), randint(5,10)))
        cbox_list += [box]
    return cbox_list

def generate_vehicles(n_vehicle):
    vehicle_list = []
    for i in range(n_vehicle):
        vehicle = create_vehicle(vendor="Abc",
                                 box_size=(randint(50,100), randint(50,100), randint(50,100)),
                                 box_max_weight=10000,
                                 cost_per_kg=10,
                                 cost_per_km=15,
                                 temp_class=Temperature.COLD,
                                 max_duration=420)
        vehicle_list += [vehicle]
    return vehicle_list

def run():
    ProblemGenerator.initialize()
    order_list = ProblemGenerator.generate_random_orders(200, 100, 10)
    vehicle_list = ProblemGenerator.generate_random_vehicles(10)
    depot_coord = ProblemGenerator.get_random_depot()
    '''
    order_list = generate_orders(200, 20)
    vehicle_list = generate_vehicles(10)
    depot_coord = tuple(lat_lon_list[10])
    '''
    for i, order in enumerate(order_list):
        #cbox_list = generate_cardboard_boxes()
        cbox_list = ProblemGenerator.get_random_duses(1000)
        # print(len(order_list[i].item_list))
        order_list[i].pack_items_into_cardboard_boxes(cbox_list)
        # print(len(order_list[i].packed_item_list))
    #problem = ProblemGenerator.generate_problem(5, 100, 10, 30)
    problem = VRP3D(vehicle_list,
                    order_list,
                    depot_coord)
                    
    solution = greedy_initialization(problem)
    print(solution.tour_list)
    # solution = 
    # print(len(unpacked_items))
    # print(med_list, box_list) 
    # print(used_box[0].packed_items)



if __name__ == "__main__":
    seed(20)
    run()