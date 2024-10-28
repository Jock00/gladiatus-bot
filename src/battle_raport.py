from settings import Settings
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse
import requests
from lxml.html import fromstring
import json
import re
from database import GladiatusDB


class BattleReport(Settings):

    def __init__(self, hour=9):
        super().__init__()

        # Get "yesterday at 9:00"
        self.yesterday_9am = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0) - timedelta(days=1)

        # Get "today at 9:00"
        self.today_9am = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)

        self.report_url += self.get_url + "?page=1&mod=reports&submod=showArena&sh=" + self.sh



    def get_highest_rewards(self, no=10):
        reports = []
        while True:

            r = requests.get(self.report_url, cookies=self.cookies, headers=self.headers)
            data = fromstring(r.text)
            elements = data.xpath("//*[@class='read']")
            done = False
            for elem in elements:
                full_data = elem.xpath(".//text()")
                full_data = [fd.strip() for fd in full_data if
                             fd.strip() and ("[" not in fd.strip() and fd.strip() != 'Details')]
                given_datetime = datetime.strptime(full_data[0], '%d.%m.%Y %H:%M:%S')
                try:
                    gold = full_data[2]
                except IndexError:
                    # is lost
                    pass
                else:

                    is_within_range = self.yesterday_9am <= given_datetime <= self.today_9am
                    if is_within_range:
                        gold = int(gold.replace(".", ""))
                        type = elem.xpath(".//@title")[0]
                        if type == "Defence":
                            continue
                        name, server = full_data[1].split()
                        server = server.replace(")", "").replace("(", "")
                        link = elem.xpath(".//@href")
                        link_player = link[0]
                        link_battle = "https://s69-en.gladiatus.gameforge.com/game/" + link[-1]
                        player = {
                            "id": link_player.split("p=")[1].split("&")[0] + '#' + server,
                            "name": name,
                            "server": server,
                            "link_player": link_player,
                            "link_battle": link_battle,
                            "date_attack": full_data[0],
                            "gold": gold,
                        }
                        reports.append(player)
                    elif given_datetime < self.yesterday_9am:
                        done = True
                        break
            if not done:
                self.report_url = re.sub(r"(page=)(\d+)", lambda match: f"{match.group(1)}{int(match.group(2)) + 1}",
                                         self.report_url)
            else:
                break
        reports = sorted(reports, key=lambda x: x['gold'], reverse=True)
        return reports[:no]


d = BattleReport()
db = GladiatusDB("players")

db.create_table()
reps = d.get_highest_rewards()
treshhold = 5000
for i in reps:
    if i["gold"] >= treshhold:
    # print(json.dumps(i, indent=4))
        db.insert_player(i)
res = db.query_players()
for j in res:
    print(json.dumps(j, indent=4))

db.close()