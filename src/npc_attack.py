import requests
from lxml.html import fromstring
from pyperclip import copy
from stats import Stats
from datetime import datetime
from settings import Settings
from urllib.parse import urlencode, urlparse
from package import Package

locations = {
    "Germany": {0: {"name":"Cave Temple", "npc": ["Cave Temple"]},
                3: {"name": "Death Hill", "npc": ["Skeleton Warrior", "Skeleton Berserker", "Lych","Necromancer Prince"]}

                }
    }
class npc_attack(Settings):
    min_health = 900
    
    params = {
        "mod": "location",
        "submod": "attack",
        "premium": "0",
    }
    
    def __init__(self):
        super().__init__()        
        self.params["sh"] = self.sh
        self.stats = Stats()
        self.stats.connect()

    def set_stage(self, location, stage):
        self.params["location"] = location
        self.params["stage"] = stage
        
    
    def attack_npcs(self, location, stage):
        
        health = self.stats.get_health()
        current_time = datetime.now()

        current_hour = current_time.hour
        current_minute = current_time.minute
        current_second = current_time.second
        
        # print(f'Expedition attack on {locations["Germany"][location]["name"]} - {locations["Germany"][location]["npc"][stage-1]}')
        
        if health > self.min_health:
            
            self.set_stage(location, stage)
           
            url = urlparse(self.post_url)._replace(query=urlencode(self.params)).geturl()
            
            r = requests.get(url, cookies=self.cookies)
            if '#errorText' in r.text:
                return "You either have to wait or you don't have enough points"
            elif 'needLogin' in r.text:
                return "You need to log in"
            else:
                
                return "Expediton attacked!"
        else:
            
            x,y = self.stats.get_heal()
            if x < 0 or y < 0:
                pkk = Package()
                pkk.move_items_to_inventory("3")
                x,y = self.stats.get_heal()
                if x < 0 or y < 0:
                    return "No heal in the inventory."
                else:
                    self.stats.heal(x, y)
                    return "Low HP. Healing .."
                
            else:
                self.stats.heal(x, y)
                return "Low HP. Healing .."

        
if __name__ == "__main__":

    location = 7
    stage = 2
    
    npc_attack = npc_attack()
    print(npc_attack.attack_npcs(location, stage))

