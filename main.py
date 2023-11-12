from random import seed

from data.problem_generator import ProblemGenerator
from vns.greedy_init import greedy_initialization
from vrp3d.vrp3d import VRP3D

def run():
    ProblemGenerator.initialize()
    order_list = ProblemGenerator.generate_random_orders(200, 100, 10)
    vehicle_list = ProblemGenerator.generate_random_vehicles(10)
    depot_coord = ProblemGenerator.get_random_depot()
    
    for i, order in enumerate(order_list):
        cbox_list = ProblemGenerator.get_random_duses(1000)
        order_list[i].pack_items_into_cardboard_boxes(cbox_list)
    problem = VRP3D(vehicle_list,
                    order_list,
                    depot_coord)
                    
    solution = greedy_initialization(problem)
    for i in range(solution.prob.num_vehicle):
        print(solution.tour_list[i])
        print(solution.distance_cost_list[i])
        print(solution.weight_cost_list[i])
    # print(solution.tour_list)

if __name__ == "__main__":
    seed(20)
    run()