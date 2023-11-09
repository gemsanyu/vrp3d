import random
import csv
import numpy as np
    
from vehicle.vehicle import create_vehicle
from item.box import Box
from item.medicine import Medicine
from order.order import Order
from vrp3d.vrp3d import VRP3D
from uuid import uuid1
import copy

class MasterRelasi:
    Relasi = {}
    def load_csv():
        with open('data/Master Relasi Modified.csv', newline='') as f:
            reader = csv.reader(f)
            temp = np.array(list(reader))[1:]
            for i in temp:
                MasterRelasi.Relasi[i[1]] = ({
                    "Kode Cabang" : i[0],
                    "Alamat" : i[2],
                    "Latitude" : i[3],
                    "Longitude" : i[4],
                    "State" : i[5],
                    "City" : i[6],
                    "Province" : i[7],
                    "Zip Code" : i[8],
                    "Channel" : i[9],
                    "Ship Method Code" : i[10],
                    "Ship Method Desc" : i[11],
                    "Delivery Area Group" : i[12],
                })

    def get_destination_coordinates():
        MasterRelasi.load_csv()
        temp = np.empty([len(MasterRelasi.Relasi)], dtype=object)
        it = 0
        for i in MasterRelasi.Relasi.values():
            temp[it] = (float(i["Latitude"]), float(i["Longitude"]))
            it += 1
        return temp
    
    def get_relasi(customer_number):
        return MasterRelasi.Relasi[customer_number]
    
    def get_random_customer():
        return random.choice(list(MasterRelasi.Relasi.items()))


class MasterCabang:
    Cabang = {}
    def load_csv():
        with open('data/Master Cabang Modified.csv', newline='') as f:
            reader = csv.reader(f)
            temp = np.array(list(reader))[1:]
            for i in temp:
                MasterCabang.Cabang[i[0]] = {
                    "Kode Cabang" : i[1],
                    "Nama Cabang" : i[2],
                    "Alamat" : i[3],
                    "Latitude" : i[4],
                    "Longitude" : i[5],
                }

    def get_depot_coordinates():
        MasterCabang.load_csv()
        temp = np.empty([len(MasterCabang.Cabang)], dtype=object)
        it = 0
        for i in MasterCabang.Cabang.values():
            temp[it] = (float(i["Latitude"]), float(i["Longitude"]))
            it += 1
        return temp


class MasterProduk:
    Produk = {}
    def load_csv():
        with open('data/Master Produk Modified.csv', newline='') as f:
            reader = csv.reader(f)
            temp = np.array(list(reader))[1:]
            for i in temp:
                MasterProduk.Produk[i[0]] = {
                    "HNA" : i[1],
                    "HET" : i[2],
                    "UOM" : i[3],
                    "Berat Gram" : i[4],
                    "Panjang Cm" : i[5],
                    "Lebar Cm" : i[6],
                    "Tinggi Cm" : i[7],
                    "Is Life Saving" : i[8],
                    "Volume Cm3" : i[9],
                    "Kategori Pengiriman" : i[10],
                }

    def get_product(product_code):
        return MasterProduk.Produk[product_code]
    
    def get_random_product():
        return random.choice(list(MasterProduk.Produk.items()))

TEMP_COLD = 0
TEMP_CHILL_LOW = 1
TEMP_CHILL_HIGH = 2
TEMP_ROOM = 3

TEMP_CLASS = {
    "01" : TEMP_COLD,
    "02-A" : TEMP_CHILL_LOW,
    "02-B" : TEMP_CHILL_HIGH,
    "03" : TEMP_ROOM,
    "1" : TEMP_COLD,
    "2-A" : TEMP_CHILL_LOW,
    "2-B" : TEMP_CHILL_HIGH,
    "3" : TEMP_ROOM,
}

class MasterKendaraan:
    Kendaraan = {}
    def load_csv():
        with open('data/Master Kendaraan.csv', newline='') as f:
            reader = csv.reader(f)
            temp = np.array(list(reader))[1:]
            for i in temp:
                MasterKendaraan.Kendaraan[i[0]] = {
                    "Jenis Kendaraan" : i[1],
                    "Max Berat Gram" : i[2],
                    "Panjang Cm" : i[3],
                    "Lebar Cm" : i[4],
                    "Tinggi Cm" : i[5],
                    "Kategori Pengiriman" : i[6],
                    "Cost Per KG" : i[7],
                    "Cost Per KM" : i[8],
                    "Vendor" : i[9],
                    "Max Duration" : i[10]
                }

    def get_vehicle(vehicle_code):
        return MasterKendaraan.Kendaraan[vehicle_code]
    
    def get_random_vehicle():
        return random.choice(list(MasterKendaraan.Kendaraan.items()))
    

class MasterDus:
    Dus = {}
    def load_csv():
        with open('data/Master Dus.csv', newline='') as f:
            reader = csv.reader(f)
            temp = np.array(list(reader))[1:]
            for i in temp:
                MasterDus.Dus[i[0]] = {
                    "Jenis Dus" : i[1],
                    "Max Berat Gram" : i[2],
                    "Panjang Cm" : i[3],
                    "Lebar Cm" : i[4],
                    "Tinggi Cm" : i[5],
                }

    def get_dus(dus_code):
        return MasterDus.Dus[dus_code]
    

    

class MapData:
    Vertices = []
    DepotIndices = []

    def initialize():
        depot_coordinates = MasterCabang.get_depot_coordinates()
        destination_coordinates = MasterRelasi.get_destination_coordinates()
        MasterDus.load_csv()

        for i in range(len(depot_coordinates)):
            MapData.DepotIndices.append(i)

        MapData.Vertices = np.concatenate((depot_coordinates, destination_coordinates))


   
    def get_random_destination_index():
        return random.randint(len(MapData.DepotIndices), len(MapData.Vertices) - 1)
    
    def get_random_destination():
        return MapData.Vertices[MapData.get_random_destination_index()]
    
    def get_random_depot_index():
        return random.randint(0, len(MapData.DepotIndices) - 1)
    
    def get_random_depot():
        return MapData.Vertices[MapData.get_random_depot_index()]


class ProblemGenerator:
    
    ORDER_COUNTER = 0
    CUSTOMER_COUNTER = 0

    def initialize():
        MasterProduk.load_csv()
        MasterKendaraan.load_csv()
        MapData.initialize()



    def generate_random_medicine_nocus():
        return ProblemGenerator.generate_random_medicine(uuid1(),uuid1(),uuid1())

    def generate_random_medicines_nocus(number_of_medicines):
        return [ProblemGenerator.generate_random_medicine_nocus() for i in range(number_of_medicines)]
    
    def generate_random_medicine(order_id, customer_id, number): 
        temps = MasterProduk.get_random_product()
        temp = temps[1]
        #return Medicine((int(float(temp["Panjang Cm"].replace(',', ''))), int(float(temp["Lebar Cm"].replace(',', ''))), int(float(temp["Tinggi Cm"].replace(',', '')))), int(float(temp["Berat Gram"].replace(',', ''))), TEMP_CLASS[temp["Kategori Pengiriman"]])
        return Medicine(order_id, customer_id, temps[0], number, temp["UOM"], (int(float(temp["Panjang Cm"].replace(',', ''))), int(float(temp["Lebar Cm"].replace(',', ''))), int(float(temp["Tinggi Cm"].replace(',', '')))), int(float(temp["Berat Gram"].replace(',', ''))), TEMP_CLASS[temp["Kategori Pengiriman"]])
    
    def generate_random_medicines(number_of_medicines, order_id, customer_id, number):
        return [ProblemGenerator.generate_random_medicine(order_id, customer_id, number) for i in range(number_of_medicines)]


    def generate_random_order(max_each_quantity, max_total_quantity):
        customer = MasterRelasi.get_random_customer()
        customer_id = customer[0]
        customer_coords = (float(customer[1]["Latitude"]), float(customer[1]["Longitude"]))
        items = []
        sum_quantity = 0
        while sum_quantity < max_total_quantity:
            current_quantity = min(max_total_quantity - sum_quantity, random.randint(1, max_each_quantity))
            sum_quantity += current_quantity
            med = ProblemGenerator.generate_random_medicine(ProblemGenerator.ORDER_COUNTER, customer_id, 1)
            for i in range(current_quantity):
                items.append(copy.deepcopy(med))

        return Order(ProblemGenerator.ORDER_COUNTER, customer_id, items, customer_coords)

    def generate_random_orders(number_of_orders, max_each_quantity, max_total_quantity):
        return [ProblemGenerator.generate_random_order(max_each_quantity, max_total_quantity) for i in range(number_of_orders)]

    def generate_random_vehicle():
        temp = MasterKendaraan.get_random_vehicle()[1]
        return create_vehicle(temp["Vendor"], (int(float(temp["Panjang Cm"])), int(float(temp["Lebar Cm"])), int(float(temp["Tinggi Cm"]))), int(float(temp["Max Berat Gram"])), int(float(temp["Cost Per KM"])), int(float(temp["Cost Per KG"])), TEMP_CLASS[temp["Kategori Pengiriman"]], int(float(temp["Max Duration"])))


    def generate_random_vehicles(number_of_vehicles):
        return [ProblemGenerator.generate_random_vehicle() for i in range(number_of_vehicles)]
    
    def get_random_dus():
        temp = random.choice(list(MasterDus.Dus.items()))[1]
        return Box((int(float(temp["Panjang Cm"])), int(float(temp["Lebar Cm"])), int(float(temp["Tinggi Cm"]))), int(float(temp["Max Berat Gram"])))
    
    def get_random_duses(number_of_duses):
        return [ProblemGenerator.get_random_dus() for i in range(number_of_duses)]


    def generate_problem(number_of_vehicles, number_of_orders, max_each_quantity, max_total_quantity):
        # problem dibagi menjadi banyak instance VRP3D berdasarkan depot
        return [VRP3D(ProblemGenerator.generate_random_vehicles(number_of_vehicles), ProblemGenerator.generate_random_orders(number_of_orders, max_each_quantity, max_total_quantity), MapData.Vertices[i]) for i in MapData.DepotIndices]