from package import Package
from settings import Settings
if __name__ == "__main__":
    Settings.server = '69'
    Settings.player_name = 'MikeOxlong'
    pkk = Package()
    inventory_ids = ["1", "2"]

    pkk.sell_items_from_inventory(inventory_ids)