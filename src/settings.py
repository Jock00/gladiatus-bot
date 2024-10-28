import configparser
import json


class Settings:
    server = None
    player_name = None
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        with open("servers.json", "r") as f:
            servers = json.loads(f.read())
        self.sh = config.get('PLAYERDATA', 'SH')
        world_code = config.get('PLAYERDATA', 'WorldCode')
        php_session = config.get('PLAYERDATA', 'PHPSession')

        self.cookies = {
            f"Gladiatus_{servers[self.server]['lang']}_{self.server}":
                f"{servers[self.server]['player'][self.player_name]}%" +
                world_code,
            "PHPSESSID": php_session,
        }

        self.post_url = config.get('LINKS', 'PostReq').format(
            server=self.server)
        # print(self.post_url)
        self.get_url = config.get('LINKS', 'GetReq').format(
            server=self.server)

        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest'
        }

    def get_data(self):
        print(self.headers)
