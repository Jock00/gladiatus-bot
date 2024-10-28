import requests
from lxml.html import fromstring
from settings import Settings

ABILITIES = {
    "Strength": '1',
    "Dexterity": '2',
    "Agility": '3',
    "Constitution": '4',
    "Charisma": '5',
    "Intelligence": '6',
    }
class Training(Settings):

    def __init__(self):
        self.train_url = self.get_url + "?mod=training&submod=train&skillToTrain={}&sh={}"
        super().__init__()
        
    
    def train(self, ability):
        ability_to_train = ABILITIES[ability]
        self.train_url = self.train_url.format(ability_to_train, self.sh)
        response = requests.get(self.train_url, cookies=self.cookies)
        if response.status_code == 200:
            print(f"Ability {ability} trained!")
       
    def get_data(self):
        url = self.get_url + "?mod=training&sh=" + self.sh
        response = requests.get(url, cookies=self.cookies)
        data = fromstring(response.text)
        base_stats = data.xpath('//*[@class="training_value"][1]//text()')
        price = data.xpath("//*[@class='training_costs']//text()")
        price = [p.strip().replace(".", "") for p in price if p.strip()]
        print(price)
        result_dict = {key: (val1, val2) for key, val1, val2 in zip(list(ABILITIES.keys()), base_stats, price)}
        return result_dict