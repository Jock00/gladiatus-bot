import requests
from lxml.html import fromstring
import numpy
import random
import json
from html import unescape
from pyperclip import copy
import time
from settings import Settings
from urllib.parse import urlparse, urlunparse, urlsplit, urlencode, parse_qs
from collections import defaultdict

class Package(Settings):
    max_x = 8
    max_y = 5

    inventory_lines = 5
    inventory_columns = 8
    inventory_shape = (inventory_lines, inventory_columns)
    data = None
    base_url = ""
    inventory_map = {
        # "4": "515",
        "3": "515",
        "2": "514",
        "1": "513",
    }

    params = {
        'mod': 'inventory',
        'submod': 'move',
        # 'from': '-8343447',
        'fromX': '1',
        'fromY': '1',
        # 'to': '513',
        # 'toX': '1',
        # 'toY': '1',
        'amount': '1',
    }
    map_name = defaultdict(dict)
    def __init__(self):
        super().__init__()
        self.package_url = self.get_url + "?page=1&mod=packages&sh=" + self.sh
        self.inventory_url = self.post_url + \
                              f"""?mod=inventory&submod=setInv&sh={self.sh} 
                              +&inv="""


    def get_package_page(self, inventory_id, page=1):
        data = parse_qs(urlparse(self.package_url).query)
        data = {k:v[0] for k,v in data.items()}

        data["page"] = str(page)
        self.package_url = urlunparse(urlparse(self.package_url)._replace(query=urlencode(data)))
        if inventory_id == '3':
            self.package_url += '&f=7'
        req = requests.get(self.package_url, cookies=self.cookies)
        data = fromstring(req.text)
        try:
            last_page = data.xpath("//*[@class='paging']//a/text()")[-1]
        except IndexError:
            return None

        if page > int(last_page):
            return None
        return fromstring(req.text)

    def get_inventory_page(self, inventory_id='513'):
        self.inventory_url += inventory_id
        req = requests.get(self.package_url, cookies=self.cookies)
        return fromstring(req.text)

    def get_inventory(self, inventory_id):
        # return the inventory as 2d array

        data = self.get_inventory_page(inventory_id)
        script_txt = 'JSON.parse'
        p = 'data-container-number'
        inventory = numpy.zeros(self.inventory_shape, dtype=int)
        script = data.xpath(f"//*[contains(text(), '{script_txt}')]//text()")[-1]
        script = unescape(script.split(script_txt)[-1]).replace("\\", "")
        scripts = script.split(p)[1:]
        for i in scripts:
            d = i.split()
            dd = {}
            name = []
            found_name = False
            for k in d:
                try:
                    k, v = k.split("=")
                except ValueError:
                    if found_name:
                        if "," in k:
                            found_name = False
                            name.append(k.split('"')[0])
                            self.map_name[dd["item_id"]]["name"] = " ".join(name)
                        name.append(k)

                v = v.replace('"', "")
                if k == "data-tooltip":
                    found_name = True
                    continue

                if not k:
                    dd["inventory_id"] = v

                if k == "data-item-id":
                    dd["item_id"] = v

                if k == "data-position-x":
                    dd["pos_x"] = int(v) - 1

                if k == "data-position-y":
                    dd["pos_y"] = int(v) - 1

                if k == "data-measurement-x":
                    dd["len_x"] = int(v)

                if k == "data-measurement-y":
                    dd["len_y"] = int(v)

                if k == "data-price-gold":
                    self.map_name[dd["item_id"]]["gold"] = int(v)

            if dd["inventory_id"] == self.inventory_map[inventory_id]:
                self.fill_empty(inventory, dd["pos_y"], dd["pos_x"], dd["len_y"], dd["len_x"], dd["item_id"])
        return inventory

    def get_seller_inventory(self, location, box='2'):
        # inventory_id [0...5]
        # return the inventory of NPC as 2d array
        rows = 8
        columns = 6

        matrix = numpy.zeros((rows, columns), dtype=int)


        new_query = {
            "mod": "inventory",
            "sub": location,
            "subsub": box,
            "sh": self.sh
        }
        url = urlparse(self.get_url)._replace(query=urlencode(new_query)).geturl()
        r = requests.get(url, cookies=self.cookies)
        data = fromstring(r.text)
        seller_id = data.xpath("//@data-container-number")[0]

        repo = data.xpath("//*[@id='shop']//div")
        for rp in repo:
            y = int(rp.xpath(".//@data-position-x")[0]) - 1
            x = int(rp.xpath(".//@data-position-y")[0]) - 1
            len_y = int(rp.xpath(".//@data-measurement-x")[0])
            len_x = int(rp.xpath(".//@data-measurement-y")[0])
            item_id = int(rp.xpath(".//@data-item-id")[0])
            self.fill_empty(matrix, x, y, len_x, len_y, item_id)
        return matrix, seller_id

    def get_size(self, matrix, pos_x, pos_y):
        initial_x = pos_x
        initial_y = pos_y
        while (pos_x < len(matrix) and matrix[pos_x][pos_y] == matrix[initial_x][initial_y]):
            pos_x += 1
        while (pos_y < len(matrix[0]) and matrix[pos_x - 1][pos_y] == matrix[initial_x][initial_y]):
            pos_y += 1
        return pos_x - initial_x, pos_y - initial_y

    def sell_items(self, inventory_id, location, box='2'):
        # sell items to NPCs. from inventory id to NPC_id - location
        items_sold = 0
        total_gold = 0
        seller, seller_id = self.get_seller_inventory(location, box)
        inventory = self.get_inventory(inventory_id)
        for row in range(0, len(inventory)):
            for column in range(0, len(inventory[0])):
                if inventory[row][column]:
                    # needs to move
                    row_size, column_size = self.get_size(inventory, row, column)
                    x, y = self.find_space(seller, row_size, column_size)
                    print(
                        f"\t\tTrying to move {inventory[row][column]} from {row, column} of size {row_size, column_size} to {x, y}")
                    if x < 0 or y < 0:
                        self.fill_empty(inventory, row, column, row_size, column_size, 0)
                        continue
                    params = {
                        'mod': 'inventory',
                        'submod': 'move',
                        'from': self.inventory_map[inventory_id],
                        'fromX': column + 1,
                        'fromY': row + 1,
                        'to': seller_id,
                        'toX': y + 1,
                        'toY': x + 1,
                        'amount': '1',
                        'doll': '1',
                    }

                    data = '&sh=' + self.sh
                    response = requests.post(
                        self.post_url,
                        params=params,
                        cookies=self.cookies,
                        headers=self.headers,
                        data=data,
                    )
                    if "error" in response.text:
                        print()
                        print("--------------------------")
                        print("Failed")
                        print(inventory[row][column])
                        print("Inventory")
                        print(inventory)
                        print("Seller")
                        print(seller)
                        print(json.dumps(params, indent=4))
                        print("----------------------")
                        print()
                    else:
                        idd = str(inventory[row][column].item())
                        total_gold += self.map_name[idd]["gold"]
                        print(f'\t\tSold {self.map_name[idd]["name"]} ({idd}) for {self.map_name[idd]["gold"]} gold')
                        self.fill_empty(seller, x, y, row_size, column_size, inventory[row][column])
                        self.fill_empty(inventory, row, column, row_size, column_size, 0)
                        # items_sold += 1
                    time.sleep(2)
        return total_gold

    def check_matrix_has_space(self, matrix):
        for line in range(self.inventory_lines):
            for column in range(self.inventory_columns):
                if not matrix[line][column]:
                    return 1
        return 0
    def check_zeros(self, matrix, x_start, y_start, x_end, y_end):
        s = 0
        for el in matrix[x_start:x_end]:
            for k in el[y_start: y_end]:
                s += k
        return s == 0

    def find_space(self, matrix, dim_x, dim_y):
        good_x, good_y = -1, -1
        for i in range(0, len(matrix) - dim_x + 1):
            for j in range(0, len(matrix[0]) - dim_y + 1):
                if self.check_zeros(matrix, i, j, i + dim_x, j + dim_y):
                    return i, j
        return good_x, good_y

    def fill_empty(self, matrix, x_start, y_start, len_x, len_y, value):
        for i in range(x_start, x_start + len_x):
            for j in range(y_start, y_start + len_y):
                matrix[i][j] = value

    def get_unique_items_id(self, matrix):
        ids = []
        for line in range(self.inventory_lines):
            for column in range(self.inventory_columns):
                elem = int(matrix[line][column])
                if elem == 0:
                    continue
                if elem not in ids:
                    ids.append(elem)
        return ids

    def move_items_to_inventory(self, inventory_id='513', package_page=1):
        # moves items from packages to inventory
        data = self.get_package_page(inventory_id, package_page)
        if data is None:
            return -1
        inventory = self.get_inventory(inventory_id)
        raw_data = data.xpath('//*[@class="packageItem"]')

        self.params['to'] = str(512 + int(inventory_id))
        send_req = 1
        moved_items = 0
        for d in raw_data:

            len_y = d.xpath(".//@data-measurement-x")[0]
            len_x = d.xpath(".//@data-measurement-y")[0]
            p_id = d.xpath(".//@data-container-number")[0]
            p_type = d.xpath(".//@data-content-type")[0]
            not_healer = "heals" in d.xpath(".//@data-tooltip")[0].lower()
            food_item_in_package = not_healer and inventory_id != '3'
            if food_item_in_package:
                continue
            x, y = self.find_space(inventory, int(len_x), int(len_y))

            if x != -1:
                self.params['from'] = p_id
                self.params['toX'] = str(int(y) + 1)
                self.params['toY'] = str(int(x) + 1)
                if send_req:
                    pp = requests.post(
                        self.post_url,
                        params=self.params,
                        cookies=self.cookies,
                        headers=self.headers,
                        data='&sh=' + self.sh,
                    )
                    if "error" in pp.text:
                        print(f"Could not move object - {self.map_name[p_id]}! Data: {json.dumps(self.params, indent=4)}")

                    else:
                        moved_items += 1
                        print(f"{p_id} moved!")
                        self.fill_empty(inventory, x, y, int(len_x), int(len_y), p_id)
            else:
                pass
                # print(f"No space for {p_id}")
        return moved_items
    def store_materials(self):
        params = {
            'mod': 'forge',
            'submod': 'storageIn',
        }

        data = {
            'inventory': '1',
            'packages': '1',
            'sell': '1',
            'sh': self.sh
        }
        response = requests.post(
            self.post_url,
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )
        if "error" in response.text:
            print("Error!")
        else:
            print("Materials moved!")

    @staticmethod
    def print_seller(seller_id):
        vendors = [
            "Weapon Smith",
            "Armour Smith",
            "General Goods",
            "Alchemist",
            "Mercenary",
            "Malefica"
        ]
        return vendors[seller_id]

    def get_new_goods(self):
        params = {
            'mod': 'inventory',
            'sub': '1',
            'subsub': '2',
            'sh': self.sh,
        }

        data = {
            'bestechen': 'New goods',
        }
        response = requests.post(
            self.get_url,
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )
        if response.status_code == 200:
            return 1
        return 0

    def fill_inventory(self, inventory_ids_arg):
        for inventory_id in inventory_ids_arg:
            page = 1
            while True:
                inventory = self.get_inventory(inventory_id)
                res = self.move_items_to_inventory(inventory_id, page)
                if res < 0:
                    break
                if self.check_matrix_has_space(inventory):
                    page += 1
                else:
                    break

    def sell_items_from_inventory(self, inventory_ids_arg):
        total_gold = 0
        sellers = [1, 2, 3, 4, 5, 6]
        while True:
            actual_gold = 0
            for inventory_id in inventory_ids_arg:
                print(f"inventory_id = {inventory_id}")
                for seller in sellers:
                    print(f"\tSeller = {Package.print_seller(seller - 1)}")
                    actual_gold += self.sell_items(inventory_id, seller)
            if not actual_gold:
                print("no more space available")
                break
            else:
                total_gold += actual_gold
        print(f"Made {total_gold} gold. GG!")


if __name__ == "__main__":
    pkk = Package()

    inventory_ids = ["1", "2"]

    # pkk.get_new_goods()

    pkk.store_materials()
    pkk.fill_inventory(inventory_ids)




