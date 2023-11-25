from random import seed
import datetime

from data.database import Database


def run():
    Database.Initialize()
    
    Database.generate_random_orders(9, 10, 150)


if __name__ == "__main__":
    seed(datetime.datetime.now().timestamp())
    run()