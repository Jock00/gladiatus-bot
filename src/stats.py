import requests
from lxml.html import fromstring
from pyperclip import copy
import json
import ast
import html
import re
from settings import Settings
from bs4 import BeautifulSoup


class Stats(Settings):
    health_bonus_map = []
    data = None
    trashhold = 200
    def __init__(self):
        super().__init__()
        self.profile_url = self.get_url + "?mod=overview&sh=" + self.sh

    def connect(self):

        r = requests.get(self.profile_url, cookies=self.cookies,
                         headers=self.headers)
        self.data = fromstring(r.text)
        return self.data

    def get_exp_points(self):
        no = self.data.xpath(
            "//*[@id='expeditionpoints_value_point']//text()"
        )[0]
        return int(no)

    def get_abilities(self, data=None):
        data = data if data is not None else self.data
        abilities = data.xpath("//*[@class='charstats_bg']//text()")
        abilities = [ab.strip() for ab in abilities if ab.strip()]
        total = {abilities[i]:abilities[i+1] for i in range(0,len(abilities),2)}
        return total
    
    def get_sum_abilities(self, abilities):
        sum_ab = int(abilities['Strength'])*0.9 + int(abilities['Dexterity'])*0.08 + int(abilities['Agility'])*0.8 + int(abilities['Constitution'])*0.1 + \
                    int(abilities['Charisma'])*0.7 + int(abilities['Intelligence'])*0.1
        return sum_ab
        
    def get_arrmor(self, abilities):
        return int(abilities["Armour"])
    
    def get_better_player(self, data=None):
        own_ability = self.get_abilities()
        enemy_abilities = self.get_abilities(data)
        # compare current player with somebody else
        current_player = {
            "sum": self.get_sum_abilities(own_ability),
            "arrmor": self.get_arrmor(own_ability)
            }
        enemy_player = {
            "sum": self.get_sum_abilities(enemy_abilities),
            "arrmor": self.get_arrmor(enemy_abilities)
            }
        own_damage = own_ability['Damage'].split("-")
        enemy_damage = enemy_abilities['Damage'].split("-")
        damage_result = (
        int(own_damage[0].strip()) - int(enemy_damage[0].strip()) +
         int(own_damage[1].strip()) - int(enemy_damage[1].strip())  
         )/2
        
        result = ( 
            current_player["sum"] - enemy_player["sum"] + 
            current_player["arrmor"] - enemy_player["arrmor"]
            ) // 10 + damage_result * 10
        return result
    
    def get_health(self):
        health_data = self.data.xpath("//*[@id='header_values_hp_bar']/@data-tooltip")[0]
        health = int(health_data.split('"')[3].split()[0])
        return health
        
    def get_heal(self):

        health_data = self.data.xpath('//script[contains(text(),"JSON.parse(")]//text()')[-1]
        health_data = health_data.split("JSON.parse(")[-1][:-1]
        data = re.sub(r'\\\\\\"', '"',html.unescape(health_data))[1:].split(")\n")[0]

        o = data.split('data-container-number="515"')

        pos_x_start = -1
        pos_y_start = -1
       
        for i in o[1:]:
            if "Using: Heals " in i:
                health = i.split('Using: Heals ')[1].split()[0]
                split_texts = i.split()
               
                for split_text in split_texts:
                    value = split_text.split("=")[-1].replace('"', "")
                    if 'data-position-x' in split_text:
                        pos_x_start = int(value)
                    elif 'data-position-y' in split_text:
                        pos_y_start = int(value)
                    if pos_x_start > 0 and pos_y_start > 0:
                        break
                break
        return pos_x_start, pos_y_start
       
    def heal(self, pos_x, pos_y, inventory = '515'):
        params = {
            'mod': 'inventory',
            'submod': 'move',
            'from': inventory,
            'fromX': str(pos_x),
            'fromY': str(pos_y),
            'to': '8',
            'toX': '1',
            'toY': '1',
            'amount': '1',
            'doll': '1',
        }
        
        data = '&sh='+self.sh
        headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',  
        }
        heal_req = requests.post(
            self.post_url,
            params=params,
            headers=headers,
            cookies=self.cookies,
            data=data,
        )
        #print(pos_x, pos_y)
        if 'Increases healing in ' in heal_req.text:
            return "Healed!"
        else:
            return "Error occured"


if __name__ == "__main__":
    pass
    statt = Stats()
    statt.connect()
    x,y = statt.get_heal()
    statt.heal(x,y)
