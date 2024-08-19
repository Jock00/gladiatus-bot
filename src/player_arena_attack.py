import requests
from lxml.html import fromstring
from stats import Stats
from pyperclip import copy
import time
from urllib.parse import parse_qs, urlparse, urlunparse
from settings import Settings
import json
from package import Package
class PlayerAttack(Settings):
    
    arena_url = "https://s69-en.gladiatus.gameforge.com/game/index.php?mod=arena&submod=serverArena&sh="
    base_post_url = "https://s69-en.gladiatus.gameforge.com/game/ajax.php"
    base_get_url = "https://s69-en.gladiatus.gameforge.com/game/index.php"
    min_health = 2500
    
    def __init__(self):
        super().__init__()
        self.arena_url += self.sh
        self.stats = Stats()
        self.params = {
                'mod': 'arena',
                'submod': 'getNewOpponents',
                'aType': '2',
                'sh': self.sh,
            }
        self.attack_url = "{}?mod=arena&submod=doCombat&opponentId={}&serverId={}&country=en&sh={}"
        self.data = {
                'actionButton': 'Search for opponents',
            }
    
    
    def find_players(self):
        def find_new_players():
            requests.post(
                self.base_get_url,
                params=self.params,
                cookies=self.cookies,
                data=self.data,
            )
            return "No worthy opponents. This round you rest in arena."

        current_player_data = self.stats.connect()
        req = requests.get(self.arena_url, cookies = self.cookies)
        data = fromstring(req.text)
        links = data.xpath("//table//td//a[@target='_blank']//@href")
        current_player = self.stats.get_better_player()
        
        max_points = (0, "", "")
        for link in links:
            player_req = requests.get(link)
            
            player_data = fromstring(player_req.text)
            player_name = player_data.xpath('//*[contains(@class, "playername")]//text()')[0].strip()
            
            k = self.stats.get_better_player(player_data)

            if k > max_points[0]:
                max_points = (k, link, player_name)
 
        if max_points[0] == 0:
            return find_new_players()

        else:
            if self.stats.get_health() > self.min_health:

                enemy_id = parse_qs(urlparse(max_points[1]).query)['p'][0]
                server_id = max_points[1].split("-")[0].split("//s")[-1]
                
                attack_url = self.attack_url.format(self.base_post_url, enemy_id, server_id, self.sh)

                d = requests.get(attack_url, cookies=self.cookies)
                if 'You have already fought' in d.text:
                    return find_new_players()
                else:
                    return f"Arena attack on **{max_points[2]}**"
            else:
                txt = "Low HP. Prepare for next round in arena. Trying to heal .."
                x,y = self.stats.get_heal()

                if x < 0 and y < 0:
                    pkk = Package()
                    pkk.move_items_to_inventory("3")
                    x,y = self.stats.get_heal()
                    if x < 0 and y < 0:
                        txt += "No items to heal in inventory. Need to buy."
                else:
                    txt += "Healed!"
                    self.stats.heal(x, y)
                return txt
              
        
if __name__ == "__main__":
    player_attack = PlayerAttack()
    response = player_attack.find_players()