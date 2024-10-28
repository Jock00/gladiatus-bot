import requests
from npc_attack import npc_attack
from stats import Stats
from inventory import Inventory
from dungeon_attack import DungeonAttack
from player_arena_attack import PlayerAttack
from package import Package
from auction import Auction
from training import Training

from settings import Settings

if __name__ == "__main__":

    Settings.server = '71'
    Settings.player_name = 'Dnme'

    # attack a player
    """
    player_attack = PlayerAttack()
    result = player_attack.find_players()
    print(result)
    """

    # expedition attack
    """
    location = 0
    stage = 1
    npc_attack = npc_attack()
    result = npc_attack.attack_npcs(location, stage)
    print(result)
    """

    # take packages and move them to inventory - does not work when its only
    # one page
    """
    pkk = Package()

    inventory_ids = ["1", "2"]

    # pkk.get_new_goods()

    pkk.store_materials()
    pkk.fill_inventory(inventory_ids)
    """

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