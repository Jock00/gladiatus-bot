import requests
from npc_attack import npc_attack
from stats import Stats
from inventory import Inventory
from dungeon_attack import DungeonAttack
from player_arena_attack import PlayerAttack
from package import Package
from auction import Auction
from training import Training

sh = "5e44af2dc71328a386351328a9b9a28d"
php_session = "65lvqle0d50smdbgalb447epj0"
url = "https://s69-en.gladiatus.gameforge.com/game/index.php?mod=highscore&sh=" + sh
abilities = ['Strength', 'Dexterity', 'Agility', 'Constitution', 'Charisma', 'Intelligence']


world_code = "3B015d535f6f00281f5e947b2e6c74e432"
cookies = {
    "Gladiatus_en_69": "22253%" + world_code,
    "PHPSESSID": php_session,
}
print()

train = Training(cookies, sh)
# train.train(abilities[3])
print(train.get_data())
#auction = Auction(cookies, sh)
#auction.buy_items()

""" - > seems to work but idk why last column and last line not working
package = Package(cookies, sh)
package.get_package()
package.get_matrix()
package.print_matrix()
# print(package.find_space(3,3))


location_npc = 6
location_dungeon = 5
type_dungeon = "Advanced"
DungeonAttack = DungeonAttack(cookies, sh, location_dungeon)

try:
    DungeonAttack.connect()
except IndexError:
    DungeonAttack.enter_dungeon(type_dungeon) # delete arg for normal dungeon
    DungeonAttack.connect()
DungeonAttack.attack()

npc_attack = npc_attack(cookies, sh)
npc_attack.connect()
npc_attack.attack_npcs(location_npc,2)




player_attack = PlayerAttack(cookies, sh)
player_attack.find_players()


stats = Stats(cookies, sh)
stats.connect()
x, y = stats.get_heal()
print(x,y)
stats.heal(x,y)


inventory = Inventory(cookies, sh, 3)
inventory.heal('1', '1')
#print(attack)
"""