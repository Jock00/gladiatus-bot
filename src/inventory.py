import requests
from stats import Stats
import json
from settings import Settings


class Inventory(Settings):
    params = {
        "mod": "inventory",
        "submod": "move",
        "to": "8",
        "toX": "1",
        "toY": "1",
        "doll": "1"
    }
    data = None
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    def __init__(self, inventory):
        super().__init__()
        self.cookies['menu_en_69'] = str(inventory + 1)
        self.base_url = self.post_url
        self.inventory_link = self.post_url + \
                              f"?mod=inventory&submod=setInv&inv={inventory}" \
                              + "&sh=" + self.sh
        self.data = "&sh=" + self.sh

    def set_inventory(self):
        x = requests.get(self.inventory_link, cookies=self.cookies)
        print(x.text)

    def heal(self, posX, posY, qt='1', inventory="515"):
        self.params['from'] = inventory
        self.params['fromX'] = posX
        self.params['fromY'] = posY
        self.params['amount'] = qt

        print(json.dumps(self.params, indent=4))
        req = requests.post(
            self.base_url,
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
            data=self.data
        )
        print(req.text)
        if '"heal"' in req.text:
            return 1
        return 0
