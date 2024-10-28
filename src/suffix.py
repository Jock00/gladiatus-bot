import requests
from lxml.html import fromstring
import json
from collections import defaultdict
from settings import Settings


def write_suffix():
    suffix_page = 'https://gladiatus.gamerz-bg.com/suffixes'
    clas = "item-page"
    r = requests.get(suffix_page)
    data = fromstring(r.text)

    tables = data.xpath(f"//*[@class='{clas}']//table")

    sufixes = {}
    for table in tables:
        try:
            name = table.xpath(".//tr[1]//td[2]//text()")[0].lower()
        except IndexError:
            print(table.xpath(".//tr[1]//td[2]//text()"))
            continue
        abilities = table.xpath(".//tr[2]//td[2]//text()")
        elem = defaultdict(list)
        for ability in abilities:
            abil = " ".join(ability.split()[:-1])
            number = ability.split()[-1]
            elem[abil].append(number)
        elem = {k: " ".join(v) for k, v in elem.items()}
        sufixes[name] = elem

    with open("suffixes.json", "w") as f:
        f.write(json.dumps(sufixes, indent=4))


class SuffixClass(Settings):
    def __init__(self):
        super().__init__()

    def get_all_suffixes(self, file_name='suffixes.json'):
        with open(file_name, "r") as f:
            return json.loads(f.read())

    def search_suffix(self, searchable_data, ability):
        good_suffixes = {}
        for suff, abilities in searchable_data.items():
            if ability in abilities:
                good_suffixes[suff] = abilities
        return good_suffixes


    def get_suffixes(self):
        url = "https://s69-en.gladiatus.gameforge.com/game/index.php?" \
              "mod=forge&submod=forge&sh=" + self.sh

        req = requests.get(url, headers=self.headers, cookies=self.cookies)
        data = fromstring(req.text)
        suffs = data.xpath("//*[@label='Suffix']//@data-name")[1:]
        data = self.get_all_suffixes()
        available_suffixes = {}
        for suff in suffs:
            if suff in data:
                available_suffixes[suff] = data[suff]
        return available_suffixes

    def get_all_avail_suffixes(self, ability):

        data = self.get_suffixes()
        return self.search_suffix(data, ability)

    def sort_results(self, ability):
        data = self.get_all_avail_suffixes(ability)
        new_data = [data.popitem()]
        for suffix in data:
            field = data[suffix][ability]
            index = 0

            if field[0] == '-':
                continue
            for vals in new_data:
                compared_field = vals[1][ability]

                if "%" in field:
                    if "%" not in compared_field:
                        break
                    else:
                        v1 = field.split()[-1][:-1]
                        v2 = compared_field.split()[-1][:-1]
                        if int(v1) > int(v2):
                            break
                        else:
                            pass
                else:
                    if "%" in compared_field:
                        pass
                    else:
                        v1 = field[1:]
                        v2 = compared_field[1:]
                        if int(v1) > int(v2):
                            break
                        else:
                            pass

                index += 1

            new_data.insert(index, (suffix, data[suffix]))


        return new_data


# write_suffix()
suffixx = SuffixClass()
ability = "Charisma"
final = suffixx.get_all_avail_suffixes(ability)
res = suffixx.sort_results(ability)
for i in res:
    print(i[0], i[1])
# print(json.dumps(final, indent=4))
