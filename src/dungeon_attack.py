import requests
from lxml.html import fromstring
from pyperclip import copy
from stats import Stats
from datetime import datetime
from settings import Settings


class DungeonAttack(Settings):

    params = {}

    def __init__(self, location):
        super().__init__()
        self.params["sh"] = self.sh

        self.location = location

        self.data = None
        self.npc_id = ""

        self.base_link = self.get_url
        self.fight_url = self.post_url + "/doDungeonFight.php"
        self.dungeon_link = self.get_url + f"?mod=dungeon&loc={location}&sh=" \
                            + self.sh

    def connect(self):

        data = requests.get(self.dungeon_link, cookies=self.cookies)
        string_text = fromstring(data.text)
        dungeon_id = string_text.xpath('//*[@name="dungeonId"]//@value')[0]
        current_time = datetime.now()

        # Extract hour, minute, and second
        current_hour = current_time.hour
        current_minute = current_time.minute
        current_second = current_time.second
        dungeon_name = \
        string_text.xpath("//*[@class='dungeon_header_open']//text()")[0]
        # print(f"Dungeon attack on: {dungeon_name}")
        self.params["did"] = dungeon_id

        npc_data = data.text.split('startFight')
        ok = True
        for el in npc_data:
            try:
                d = el.split(',')[0].replace('(', "").replace("'", "")
            except IndexError:
                pass
            else:
                if d[0].isdigit():
                    self.npc_id = d
                    ok = False
            if not ok:
                break

    def attack(self):
        if self.npc_id:
            self.params['posi'] = self.npc_id
            response = requests.get(
                self.fight_url,
                params=self.params,
                cookies=self.cookies,

            )
            return "Dungeon attacked!"
            self.npc_id = ""
        else:
            return "You either jave to wait or you don't have enough points"

    def enter_dungeon(self, difficulty='Advanced'):
        # print("Entering dungeon ..")
        params = {
            'mod': 'dungeon',
            'loc': self.location,
            'sh': self.sh,
        }

        data = {
            'dif2': difficulty,
        }
        requests.post(
            self.base_link,
            params=params,
            cookies=self.cookies,
            data=data,
        )


if __name__ == "__main__":
    location = 3
    type_dungeon = 'Advanced'
    dungeon_attack = DungeonAttack(location)
    try:
        dungeon_attack.connect()
    except IndexError:
        dungeon_attack.enter_dungeon(
            type_dungeon)  # delete arg for normal dungeon
        dungeon_attack.connect()
    response = dungeon_attack.attack()
    print(response)
