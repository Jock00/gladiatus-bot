import json
import requests
from lxml.html import fromstring
from settings import Settings


class Auction(Settings):
    data = {
        'doll': '1',
        'qry': '',
        # 'itemLevel': '63',
        # 'itemType': '7',
        'itemQuality': '-1',
    }
    params_place_bid = {
        'mod': 'auction',
        'submod': 'placeBid',
        'ttype': '2',
        'rubyAmount': '',
    }
    data_place_bid = {
        'qry': '',
        'itemQuality': '-1',
        'buyouthd': '0',
        'bid': 'Bid',
    }

    def __init__(self, itemLevel='63', itemType='7', time='very short'):
        super().__init__()
        self.data['itemLevel'] = itemLevel
        self.data['itemType'] = itemType
        self.params = {
            'mod': 'auction',
            'sh': self.sh,
        }
        self.auction_url = self.get_url
        self.params_place_bid['sh'] = self.sh
        self.time = time

    def buy_items(self):
        response = requests.post(
            self.auction_url,
            params=self.params,
            cookies=self.cookies,
            data=self.data,
        )
        data = fromstring(response.text)
        time = data.xpath('//*[@class="description_span_right"]//text()')[0]
        if time.lower() == self.time:
            elements = data.xpath('//*[@id="auction_table"]//td')
            txt = []
            for elem in elements:

                try:
                    info = elem.xpath(".//@data-tooltip")[0]
                except IndexError:
                    pass
                else:
                    team_mate = elem.xpath(
                        ".//*[@class='auction_bid_div']//div[1]//@href")
                    if team_mate:
                        continue

                    auction_id = elem.xpath('.//*[@name="auctionid"]//@value')[
                        0]
                    item_type = elem.xpath('.//*[@name="itemType"]//@value')[0]
                    item_level = elem.xpath('.//*[@name="itemLevel"]//@value')[
                        0]
                    item_price = elem.xpath('.//*[@name="bid_amount"]//@value')[
                        0]
                    name_data = json.loads(info)[0]
                    name = name_data[0][0], name_data[1][0]

                    self.data_place_bid['auctionid'] = auction_id
                    self.data_place_bid['itemType'] = item_type
                    self.data_place_bid['itemLevel'] = item_level
                    self.data_place_bid['bid_amount'] = item_price

                    response = requests.post(
                        self.auction_url,
                        params=self.params_place_bid,
                        cookies=self.cookies,

                        data=self.data_place_bid,
                    )
                    txt.append(
                        f"Bid for '{name[0]}' ({name[1].split(':')[-1].strip()}) - price: {item_price}" + "\n")
            return txt
        else:
            return [
                f"You have to wait. Current time is {time.lower()}. Try again when is **{self.time}**"]


if __name__ == "__main__":
    auction_action = Auction()
    for i in auction_action.buy_items():
        print(i)
