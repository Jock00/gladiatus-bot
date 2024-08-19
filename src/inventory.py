import requests
from stats import Stats
import json

class Inventory:
    inventory_link = "https://s69-en.gladiatus.gameforge.com/game/ajax.php?mod=inventory&submod=setInv&inv={}&sh="
    drag_item_link = "https://s69-en.gladiatus.gameforge.com/game/ajax.php?mod=inventory&submod=move&from={}&fromX={}&fromY={}&to=8&toX=1&toY=1&amount=1&doll=1"
    base_url = "https://s69-en.gladiatus.gameforge.com/game/ajax.php"
    params = {
        "mod": "inventory",
        "submod": "move",
        "to": "8",
        "toX": "1",
        "toY": "1",
        "doll": "1"
    }
    data = None
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    
    def __init__(self, cookies, sh, inventory):
        self.cookies = cookies
        self.cookies['menu_en_69'] = str(inventory+1)
        self.inventory_link = self.inventory_link.format(inventory) + sh
        self.data = "&sh="+sh
        
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
        
    
   