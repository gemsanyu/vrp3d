from random import seed

from data.problem_generator import ProblemGenerator
from vns.greedy_init import greedy_initialization
from vrp3d.vrp3d import VRP3D

def run():
    ProblemGenerator.initialize()
    kode_cabang, depot_coord = ProblemGenerator.get_random_depot()
    order_list = ProblemGenerator.generate_random_orders(50, 5, 10, kode_cabang)
    vehicle_list = ProblemGenerator.generate_random_vehicles(3)
    
    
    for i, order in enumerate(order_list):
        cbox_list = ProblemGenerator.get_random_duses(1000)
        order_list[i].pack_items_into_cardboard_boxes(cbox_list)
        print(i)
        print(len(order_list[i].packed_item_list))
    problem = VRP3D(vehicle_list,
                    order_list,
                    depot_coord)
                    
    solution = greedy_initialization(problem)
    problem.reset(solution)
    for i in range(solution.num_vehicle):
        print(solution.tour_list[i])
        print(problem.distance_cost_list[i])
        print(problem.weight_cost_list[i])
    # print(solution.tour_list)

if __name__ == "__main__":
    seed(20)
    run()