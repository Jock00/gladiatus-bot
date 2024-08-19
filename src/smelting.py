from package import Package
from settings import Settings
import requests
from urllib.parse import urlencode, urlparse, urlunparse
import json


class Smelt(Settings):
    status = {}

    def __init__(self):
        super().__init__()

    def calculate_smelt_status(self):
        """
        :return a list of inventory for smelting; each element is empty or "finished-..
        """
        query = {
            "mod": "forge",
            "submod": "smeltery",
            "sh": self.sh
        }
        url = urlunparse(urlparse(self.get_url)._replace(query=urlencode(query)))
        request = requests.get(url, cookies=self.cookies, headers=self.headers)
        script = request.text.split("var slotsData")[-1].strip()[1:].split("var mode")[0].strip()[:-1]
        data = json.loads(script)

        slot = 0
        for elem in data:
            self.status[slot] = elem.get("state", "empty")
            slot += 1

    def smelt_item(self, item_id, slot):
        params = {
            'mod': 'forge',
            'submod': 'rent',
        }
        data = {
            'mod': 'forge',
            'submod': 'rent',
            'mode': 'smelting',
            'slot': f'{slot}',
            'rent': '2',
            'item': f'{item_id}',
            'sh': self.sh,
        }
        response = requests.post(
            self.post_url,
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )
        if response.text.strip() and "Not possible" in response.text:
            return 0
        return 1

    def get_resource_smelt(self, slot):
        params = {
            'mod': 'forge',
            'submod': 'storeSmelted',
        }

        data = {
            'mod': 'forge',
            'submod': 'storeSmelted',
            'mode': 'smelting',
            'slot': f'{slot}',
            'sh': self.sh,
        }
        _ = requests.post(
            self.post_url,
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )
        return True

    def take_resources_finished_smelting(self):
        finished_smelting = [slot for slot, status in self.status.items() if "finished" in status]
        print(finished_smelting)
        for seller in finished_smelting:
            self.status[seller] = "empty"
            smelt.get_resource_smelt(seller)
            print(f"Slot {seller} finished!")

    def put_items_in_slots(self, sellers=6, inventory_id='1'):
        pkk = Package()
        inventory_map = pkk.get_inventory(inventory_id)

        # put items to smelt
        items_to_smelt = pkk.get_unique_items_id(inventory_map)
        available_slots = [slot for slot, status in self.status.items() if status == "empty"]
        current_index_item = 0
        for item in available_slots:
            while True:
                smelting_result = smelt.smelt_item(items_to_smelt[current_index_item], item)

                if smelting_result == 1:
                    print(f"{items_to_smelt[item]} inserted on {item + 1}")
                    sellers -= 1
                    break
                else:
                    if current_index_item < len(items_to_smelt) - 1:
                        current_index_item += 1
                        print(f"{items_to_smelt[current_index_item]} not good!")
                    else:
                        if inventory_id == '1':
                            print("Changed the inventory")
                            inventory_id = '2'
                            inventory_map = pkk.get_inventory(inventory_id)
                            items_to_smelt = pkk.get_unique_items_id(inventory_map)
                            current_index_item = 0
                        else:
                            print("No more items on inventory.")
                            break


if __name__ == "__main__":
    smelt = Smelt()

    # get the availability of slots
    smelt.calculate_smelt_status()

    # finish smelting
    smelt.take_resources_finished_smelting()

    # put items to smelt
    smelt.put_items_in_slots()
