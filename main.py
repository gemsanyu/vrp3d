from random import seed

from item.box import Box
from data.problem_generator import ProblemGenerator
from vns.saving import saving
from vns.repack import repack
from vns.route_dp import improve_tours_by_dp
from vrp3d.vrp3d import VRP3D


def run():
    ProblemGenerator.initialize()
    kode_cabang, depot_coord = ProblemGenerator.get_random_depot()
    order_list = ProblemGenerator.generate_random_orders(10, 3, 10, kode_cabang)
    vehicle_list = ProblemGenerator.generate_random_vehicles(2)
    
    cbox_type_list = ProblemGenerator.get_all_duses(1)
    cbox_type_list = sorted(cbox_type_list, key=lambda box: box.volume)    
    for i, order in enumerate(order_list):
        print("Packing order ",i," into cardboxes")
        order_list[i].pack_items_into_cardboard_boxes(cbox_type_list)

    problem = VRP3D(vehicle_list,
                    order_list,
                    depot_coord)
    print("START SOLUTION GENERATION")

                    
    solution = saving(problem)
    # problem.reset(solution)
    # for i in range(solution.num_vehicle):
    #     problem.vehicle_list[i].box.visualize_packed_items()
    
    solution = improve_tours_by_dp(solution, problem)
    
    # solution = repack(solution,problem)
    # for i in range(solution.num_vehicle):
    #     problem.vehicle_list[i].box.visualize_packed_items()
    


if __name__ == "__main__":
    seed(20)
    run()