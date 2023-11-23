import copy
import csv
import random
from typing import List, Tuple
from uuid import uuid1
from datetime import datetime

import numpy as np
    
from item.box import Box
from item.cardboard import Cardboard
from item.medicine import Medicine
from order.order import Order
from vehicle.vehicle import create_vehicle
from vrp3d.vrp3d import VRP3D



import mysql.connector

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


class DBRelation:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.branch_id = db_result[1]
        self.number = db_result[2]
        self.latitude = db_result[3]
        self.longitude = db_result[4]
        self.address = db_result[5]
        self.city = db_result[6]
        self.state = db_result[7]
        self.province = db_result[8]
        self.zip_code = db_result[9]
        self.channel = db_result[10]
        self.ship_method_code = db_result[11]
        self.ship_method_desc = db_result[12]
        self.delivery_area_group = db_result[13]

    def dump(self):
        return (
            self.id,
            self.branch_id,
            self.number,
            self.latitude,
            self.longitude,
            self.address,
            self.city,
            self.state,
            self.province,
            self.zip_code,
            self.channel,
            self.ship_method_code,
            self.ship_method_desc,
            self.delivery_area_group
        )



class DBBranch:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.code = db_result[1]
        self.name = db_result[2]
        self.address = db_result[3]
        self.latitude = db_result[4]
        self.longitude = db_result[5]

    def dump(self):
        return (
            self.id,
            self.code,
            self.name,
            self.address,
            self.latitude,
            self.longitude
        )


class DBProduct:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.code = db_result[1]
        self.HNA = db_result[2]
        self.HET = db_result[3]
        self.UOM = db_result[4]
        self.weight = db_result[5]
        self.length = db_result[6]
        self.width = db_result[7]
        self.height = db_result[8]
        self.is_life_saving = db_result[9]
        self.volume = db_result[10],
        self.delivery_category = db_result[11]

    def dump(self):
        return (
            self.id,
            self.code,
            self.HNA,
            self.HET,
            self.UOM,   
            self.weight,
            self.length,
            self.width,
            self.height,
            self.is_life_saving,
            self.volume,
            self.delivery_category
        )



class DBVehicle:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.type = db_result[1]
        self.max_weight = db_result[2]
        self.length = db_result[3]
        self.width = db_result[4]
        self.height = db_result[5]
        self.delivery_category = db_result[6]
        self.cost_per_kg = db_result[7]
        self.cost_per_km = db_result[8]
        self.vendor = db_result[9]
        self.max_duration = db_result[10]
        self.driver_id = db_result[11]

    def dump(self):
        return (
            self.id,
            self.type,
            self.max_weight,
            self.length,
            self.width,
            self.height,
            self.delivery_category,
            self.cost_per_kg,
            self.cost_per_km,
            self.vendor,
            self.max_duration,
            self.driver_id,
        )


    

class DBCardboardBox:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.code = db_result[1]
        self.length = db_result[2]
        self.width = db_result[3]
        self.height = db_result[4]
        self.volume = db_result[5]
        self.max_weight = db_result[6]
        self.details = db_result[7]

    def dump(self):
        return (
            self.id,
            self.code,
            self.length,
            self.width,
            self.height,
            self.volume,
            self.max_weight,
            self.details
        )


    

class DBDeliveryCategory:
    def __init__(self, db_result: Tuple):
        self.delivery_category = db_result[0]
        self.temperature_detail = db_result[1]
        self.temperature_min = db_result[2]
        self.temperature_max = db_result[3]

    def dump(self):
        return (
            self.delivery_category,
            self.temperature_detail,
            self.temperature_min,
            self.temperature_max
        )

class DBDriver:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.name = db_result[1]

    def dump(self):
        return (
            self.id,
            self.name
        )

class DBAvailableVehicle:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.vehicle_id = db_result[1]
        self.available_date = db_result[2]

    def dump(self):
        return (
            self.id,
            self.vehicle_id,
            self.available_date,
        )

class DBDeliveryOrder:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.driver_id = db_result[1]
        self.branch_id = db_result[2]
        self.dispatch_date = db_result[3]
        self.status = db_result[4]

    def dump(self):
        return (
            self.id,
            self.driver_id,
            self.branch_id,
            self.dispatch_date,
            self.status
        )

class DBOrders:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.relation_id = db_result[1]
        self.branch_id = db_result[2]
        self.delivery_order_id = db_result[3]

    def dump(self):
        return (
            self.id,
            self.relation_id,
            self.branch_id,
            self.delivery_order_id,
        )

class DBOrderDetail:
    def __init__(self, db_result: Tuple):
        self.order_id = db_result[0]
        self.product_id = db_result[1]
        self.quantity = db_result[2]

    def dump(self):
        return (
            self.order_id,
            self.product_id,
            self.quantity
        )

class DBRouteData:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.visitation_order = db_result[1]
        self.relation_id = db_result[2]
        self.departure_time = db_result[3]
        self.delivered_time = db_result[4]

    def dump(self):
        return (
            self.id,
            self.visitation_order,
            self.relation_id,
            self.departure_time,
            self.delivered_time
        )

class DBDeliveryTrouble:
    def __init__(self, db_result: Tuple):
        self.id = db_result[0]
        self.driver_id = db_result[1]
        self.trouble_type = db_result[2]
        self.details = db_result[3]

    def dump(self):
        return (
            self.id,
            self.driver_id,
            self.trouble_type,
            self.details
        )




class Database:
    Database = None
    Cursor = None

    RELATION = "RELATION"
    BRANCH = "BRANCH"
    PRODUCT = "PRODUCT"
    VEHICLE = "VEHICLE"
    CARDBOARD_BOX = "CARDBOARDBOX"
    DELIVERY_CATEGORY = "DELIVERYCATEGORY"
    DRIVER = "DRIVER"
    AVAILABLE_VEHICLE = "AVAILABLEVEHICLE"
    DELIVERY_ORDER = "DELIVERYORDER"
    ORDERS = "ORDERS"
    ORDER_DETAIL = "ORDERDETAIL"
    ROUTE_DATA = "ROUTEDATA"
    DELIVERY_TROUBLE = "DELIVERYTROUBLE"

    DBType = {
        RELATION : DBRelation,
        BRANCH : DBBranch,
        PRODUCT : DBProduct,
        VEHICLE : DBVehicle,
        CARDBOARD_BOX : DBCardboardBox,
        DELIVERY_CATEGORY : DBDeliveryCategory,
        DRIVER : DBDriver,
        AVAILABLE_VEHICLE : DBAvailableVehicle,
        DELIVERY_ORDER : DBDeliveryOrder,
        ORDERS : DBOrders,
        ORDER_DETAIL : DBOrderDetail,
        ROUTE_DATA : DBRouteData,
        DELIVERY_TROUBLE : DBDeliveryTrouble
    }

    DRIVER_ID = "DRIVER_ID"
    ORDER_ID = "ORDER_ID"
    PRODUCT_ID = "PRODUCT_ID"
    RELATION_ID = "RELATION_ID"
    DELIVERY_ORDER_ID = "DELIVERY_ORDER_ID"
    BRANCH_ID = "BRANCH_ID"


    def Initialize():
        Database.Database = mysql.connector.connect(
            host="localhost",
            user="MediTransit",
            password="MedTrans", 
            database='MediTransit',
            auth_plugin='mysql_native_password'
        )
        
        Database.Cursor = Database.Database.cursor()

    def dump_to_database(table, entries):
        for entry in entries:
            temp = ""
            for attr in entry:
                temp += "'" + str(attr) + "',"
            Database.Cursor.execute(f"insert into {table} values ({temp[:-1]})")
        Database.Database.commit()

    def get_all(table):
            Database.Cursor.execute(f"select * from {table}")
            myresult = Database.Cursor.fetchall()
            
            ret = []
            for res in myresult:
                ret.append(Database.DBType[table](res))

            return ret
    
    def get_by_ids(table, ids):
        temp = ""
        for id in ids:
            temp += "'" + str(id) + "',"
        Database.Cursor.execute(f"select * from {table} where id in ({temp[:-1]})")
        myresult = Database.Cursor.fetchall()
        
        ret = []
        for res in myresult:
            ret.append(Database.DBType[table](res))

        return ret
    
    def get_max_id(table):
        Database.Cursor.execute(f"select max(id) from {table}")
        myresult = Database.Cursor.fetchall()[0][0]
        if myresult is None:
            myresult = 0

        return myresult
    

    def get_by_foreign_keys(table, foreign_key_strings, foreign_keys):
        temp = ""
        for i, foreign_key_string in enumerate(foreign_key_strings):
            temp += foreign_key_string + " in (" 
            for foreign_key in foreign_keys[i]:
                temp += "'" + str(foreign_key) + "',"
            temp = temp[:-1] + ") and "
        temp = temp[:-6] + ")"
        print(temp)
        print(f"select * from {table} where {temp}")
        Database.Cursor.execute(f"select * from {table} where {temp}")
        myresult = Database.Cursor.fetchall()
        
        ret = []
        for res in myresult:
            ret.append(Database.DBType[table](res))

        return ret
    

    
    
    def random_depot():
        depot = random.choice(Database.get_all(Database.BRANCH))
        coord = [depot.latitude, depot.longitude]
        kode_cabang = depot.code
        return kode_cabang, coord
    
    def get_medicine(product_id, order_id, customer_id, number):
        med = Database.get_by_ids(Database.PRODUCT, [product_id])[0]
        size = np.asanyarray([med.length,med.width,med.height], dtype=np.int64)
        return Medicine(med.id, str(order_id), str(customer_id), str(med.id), number, med.UOM, size, int(float(med.weight)), TEMP_CLASS[med.delivery_category])
    

    def random_medicine(order_id, customer_id, number): 
        med = random.choice(Database.get_all(Database.PRODUCT))
        size = np.asanyarray([med.length,med.width,med.height], dtype=np.int64)
        print(med.delivery_category)
        return Medicine(med.id, str(order_id), str(customer_id), str(med.id), number, med.UOM, size, int(float(med.weight)), TEMP_CLASS[med.delivery_category])
    
    def random_medicines(number_of_medicines, order_id, customer_id, number):
        return [Database.random_medicine(order_id, customer_id, number) for i in range(number_of_medicines)]



    def random_order(max_each_quantity, max_total_quantity, kode_cabang):
        customer = random.choice(Database.get_all(Database.RELATION))
        items = []
        sum_quantity = 0
        last_order_id = Database.get_max_id(Database.ORDERS) + 1
        while sum_quantity < max_total_quantity:
            current_quantity = min(max_total_quantity - sum_quantity, random.randint(1, max_each_quantity))
            sum_quantity += current_quantity
            med = Database.random_medicine(last_order_id, customer.id, 0)
            for i in range(current_quantity):
                new_med = copy.deepcopy(med)
                new_med.number = i
                items.append(copy.deepcopy(new_med))
        return Order(last_order_id, customer.id, items, (customer.latitude, customer.longitude))

    def random_orders(number_of_orders, max_each_quantity, max_total_quantity, kode_cabang):
        return [Database.random_order(max_each_quantity, max_total_quantity, kode_cabang) for i in range(number_of_orders)]


    def random_available_vehicles(number_of_vehicles):
        vehicles = Database.get_all(Database.AVAILABLE_VEHICLE)
        random.shuffle(vehicles)
        vehicles2 = Database.get_by_foreign_keys(Database.VEHICLE, ["ID"], [[vec.vehicle_id for vec in vehicles]])
        vecs = [create_vehicle(vec.vendor, np.asanyarray([vec.length,vec.width,vec.height], dtype=np.int64), 
                               vec.max_weight, vec.cost_per_km, vec.cost_per_kg, TEMP_CLASS[vec.delivery_category], vec.max_duration, vec.type, vec.id) for vec in vehicles2[:number_of_vehicles]]
        return vecs
    
    def random_dus():
        dus = random.choice(Database.get_all(Database.CARDBOARD_BOX))
        size = np.asanyarray([dus.length,dus.width,dus.height], dtype=np.int64)
        return Box(size, dus.max_weight, dus.code)
    
    def random_duses(number_of_duses):
        return [Database.random_dus() for i in range(number_of_duses)]

    def get_all_duses(num_each_dus_size=100) -> List[Cardboard]:
        all_dustype_list = Database.get_all(Database.CARDBOARD_BOX)
        duses = []
        for i in range(len(all_dustype_list)):
            dustype = all_dustype_list[i]
            for j in range(num_each_dus_size):
                size = np.asanyarray([dustype.length,dustype.width,dustype.height], dtype=np.int64)
                dus = Cardboard(dustype.id, dustype.code, dustype.details, size, dustype.max_weight)
                duses += [dus]
        return duses


    def generate_available_vehicles(number_of_vehicle):
        vehicles = Database.get_all(Database.VEHICLE)
        random.shuffle(vehicles)
        generated_vehicles = vehicles[:number_of_vehicle]

        last_avail_vehicle_id = Database.get_max_id(Database.AVAILABLE_VEHICLE) + 1
        for vehicle in generated_vehicles:
            avail_vehicle = DBAvailableVehicle((last_avail_vehicle_id, vehicle.id, datetime.now())).dump()
            last_avail_vehicle_id += 1
            Database.dump_to_database(Database.AVAILABLE_VEHICLE, [avail_vehicle])
        


    def generate_problem(number_of_vehicles, number_of_orders, max_each_quantity, max_total_quantity):
        return VRP3D(ProblemGenerator.generate_random_vehicles(number_of_vehicles), ProblemGenerator.generate_random_orders(number_of_orders, max_each_quantity, max_total_quantity), MapData.get_random_depot())
        

