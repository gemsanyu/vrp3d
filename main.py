from random import randint

from vehicle.box import Box
from vehicle.item import Item


def run():
    n_items = 20
    items = [Item(size=(randint(1,5), randint(1,5), randint(1,5)), weight=randint(2,10), temp_class=1) for i in range(n_items)]
    box = Box(max_weight=1000, size=(10,10,10))
    items_not_packed = box.pack_items_to_box(items, False)
    print(items_not_packed)
    print(box.packed_items)
    # box.plot_packed_items()

if __name__ == "__main__":
    run()