import configparser


class Settings:
    def __init__(self):
    
        config = configparser.ConfigParser()
        config.read('../config.ini')
        
        self.sh = config.get('PLAYERDATA', 'SH')
        world_code = config.get('PLAYERDATA', 'WorldCode')
        php_session = config.get('PLAYERDATA', 'PHPSession')
        
        
        self.cookies = {
        "Gladiatus_en_69": "22253%" + world_code,
        "PHPSESSID": php_session,
        }
        
        self.post_url = config.get('LINKS', 'PostReq')
        self.get_url = config.get('LINKS', 'GetReq')
        
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest'
            }
    def get_data(self):
        print(self.headers)