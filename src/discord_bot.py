import discord
from discord.ext import commands
from npc_attack import npc_attack
from dungeon_attack import DungeonAttack
from stats import Stats
from player_arena_attack import PlayerAttack
from auction import Auction
from crontab import CronTab 
from dotenv import load_dotenv
import os
from package import Package
from smelting import Smelt
from battle_raport import BattleReport
from database import GladiatusDB

guild_id = "1250688599318335610"

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN_DISCORD")

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)
cron = CronTab(True)
@bot.command(name='attack_player')
async def attack(ctx):
    response = "Player attack process started. "
    await ctx.send(response)
    player_attack = PlayerAttack()
    response = player_attack.find_players()
    await ctx.send(response)

@bot.command(name='attack_player_loop')
async def attack_loop(ctx):
    response = "Player looping attack process started. "
    await ctx.send(response)

    command = ("cd /home/ubuntu/gladiatus-bot/src/ && "
               "/home/ubuntu/gladiatus-bot/venv/bin/python3 /home/ubuntu/gladiatus-bot/src/player_arena_attack.py "
               ">> /home/ubuntu/gladiatus-bot/logs/player.log 2>&1")
    job = cron.new(command)
    job.minute.every(1) 
   
    cron.write()
    await ctx.send("Done")


@bot.command(name='attack_player_loop_remove')
async def remove_loop_attack(ctx):
    
    to_be_deleted = [crn for crn in cron if "player_arena_attack" in crn.command]
    for delete_cron in to_be_deleted:
        cron.remove(delete_cron)
    cron.write()

@bot.command(name='get_cron')
async def get_crons(ctx):
    for i in cron:
        data = str(i)
        if "gladiatus-bot" not in data:
            continue
        try:
            first_part, second_part = data.split(">>")
        except ValueError:
            continue
        else:
            time = first_part.split("cd")[0].strip()
            script = first_part.split("/")[-1]
            output = second_part.split()[0].strip().split("/")[-1]
            # print(time + " " + script + " "+ output)
            message = f"Script {script} is running {time} and output is {output}"
        await ctx.send(message)

@bot.command(name='attack_npc')
async def attack_npc(ctx, location=5, stage=2):
    response = "NPC attack process started. "
    await ctx.send(response)
    attack = npc_attack()
    response = attack.attack_npcs(location, stage)
    await ctx.send(response)

@bot.command(name='attack_npc_loop')
async def attack_npc_loop(ctx):
    response = "NPC attack loop process started. "
    await ctx.send(response)
    command = ("cd /home/ubuntu/gladiatus-bot/src/ && "
               "/home/ubuntu/gladiatus-bot/venv/bin/python3 /home/ubuntu/gladiatus-bot/src/npc_attack.py "
               ">> /home/ubuntu/gladiatus-bot/logs/npc.log 2>&1")
    job = cron.new(command)
    job.minute.every(1)

    cron.write()
    await ctx.send("Done")


@bot.command(name='attack_npc_loop_remove')
async def remove_loop_attack(ctx):
    to_be_deleted = [crn for crn in cron if "npc_attack" in crn.command]
    for delete_cron in to_be_deleted:
        cron.remove(delete_cron)
    cron.write()

@bot.command(name='attack_dungeon')
async def attack_dungeon(ctx, location):
    response = "Dungeon attack process started. "
    type_dungeon = "Advanced"
    await ctx.send(response)
    dungeon_attack = DungeonAttack(location)
    try:
        dungeon_attack.connect()
    except IndexError:
        dungeon_attack.enter_dungeon(type_dungeon) # delete arg for normal dungeon
        dungeon_attack.connect()
    response = dungeon_attack.attack()
    await ctx.send(response)

@bot.command(name='attack_dungeon_loop')
async def attack_dungeon_loop(ctx):
    response = "Dungeon loop attack process started. "
    await ctx.send(response)

    command = ("cd /home/ubuntu/gladiatus-bot/src/ && "
               "/home/ubuntu/gladiatus-bot/venv/bin/python3 /home/ubuntu/gladiatus-bot/src/dungeon_attack.py "
               ">> /home/ubuntu/gladiatus-bot/logs/dungeon.log 2>&1")

    job = cron.new(command=command)
    job.minute.every(1) 
   
    cron.write()
    await ctx.send("Done")

@bot.command(name='attack_dungeon_loop_remove')
async def attack_dungeon_loop_remove(ctx):
    to_be_deleted = [crn for crn in cron if "dungeon_attack" in crn.command]
    for delete_cron in to_be_deleted:
        cron.remove(delete_cron)
    cron.write()

@bot.command(name='heal')
async def heal(ctx):
    response = "Healing process started. "
    await ctx.send(response)
    stats = Stats()
    stats.connect()
    x,y = stats.get_heal()
    response = stats.heal(x, y)
    await ctx.send(response)

@bot.command(name='start_auction')
async def auction(ctx, *, time: str = 'very short'):
    response = "Looking for items at the auction .. "
    await ctx.send(response)
    time = time.replace("_", " ")
    auction = Auction(time=time)
    responses = auction.buy_items()
    for response in responses:
        await ctx.send(response)

@bot.command(name='start_loop_auction')
async def start_loop_auction(ctx, time = "very short"):
    response = "Auction with {time} started. Looping .."
    await ctx.send(response)
    command = ("cd /home/ubuntu/gladiatus-bot/src/ && "
               "/home/ubuntu/gladiatus-bot/venv/bin/python3 /home/ubuntu/gladiatus-bot/src/auction.py "
               ">> /home/ubuntu/gladiatus-bot/logs/auction.log 2>&1")
    job = cron.new(command)
    job.minute.every(1) 
   
    cron.write()
    await ctx.send("Done")
    
@bot.command(name='stop_loop_auction')
async def stop_loop_auction(ctx):
    to_be_deleted = [crn for crn in cron if "auction" in crn.command]
    for delete_cron in to_be_deleted:
        print(f"{delete_cron} removed!")
        cron.remove(delete_cron)
    cron.write()

# package
@bot.command(name='inventory_fill')
async def inventory_fill(ctx):
    response = "Filling inventory"
    await ctx.send(response)
    command = ("cd /home/ubuntu/gladiatus-bot/src/ && "
               "/home/ubuntu/gladiatus-bot/venv/bin/python3 /home/ubuntu/gladiatus-bot/src/package.py "
               ">> /home/ubuntu/gladiatus-bot/logs/package.log 2>&1")
    job = cron.new(command)
    job.hour.every(12)

    cron.write()
    await ctx.send("Done! Set to every 12h")


@bot.command(name='inventory_fill_stop')
async def inventory_fill_stop(ctx):
    to_be_deleted = [crn for crn in cron if "inventory" in crn.command]
    for delete_cron in to_be_deleted:
        print(f"{delete_cron} removed!")
        cron.remove(delete_cron)
    cron.write()

# only once
@bot.command(name='incentory_fill_once')
async def inventory_fill_once(ctx):
    response = "Filling inventory process started. "
    await ctx.send(response)
    pkk = Package()
    pkk.store_materials()
    pkk.fill_inventory(["1", "2"])

    await ctx.send("Filled!")

# selling
@bot.command(name='inventory_sell')
async def inventory_sell(ctx):
    response = "Selling inventory"
    await ctx.send(response)
    command = ("cd /home/ubuntu/gladiatus-bot/src/ && "
               "/home/ubuntu/gladiatus-bot/venv/bin/python3 /home/ubuntu/gladiatus-bot/src/sell_items.py "
               ">> /home/ubuntu/gladiatus-bot/logs/sell.log 2>&1")
    job = cron.new(command)
    job.day.every(1)

    cron.write()
    await ctx.send("Done! everyday")


@bot.command(name='inventory_sell_stop')
async def inventory_sell_stop(ctx):
    to_be_deleted = [crn for crn in cron if "sell" in crn.command]
    for delete_cron in to_be_deleted:
        print(f"{delete_cron} removed!")
        cron.remove(delete_cron)
    cron.write()

# only once
@bot.command(name='inventory_sell_once')
async def inventory_fill_once(ctx):
    response = "Selling inventory process started. "
    await ctx.send(response)
    pkk = Package()
    inventory_ids = ["1", "2"]
    pkk.sell_items_from_inventory(inventory_ids)

    await ctx.send("Sold!")

# smelting
@bot.command(name='inventory_smelt')
async def inventory_smelt(ctx):
    response = "Smelting inventory"
    await ctx.send(response)
    command = ("cd /home/ubuntu/gladiatus-bot/src/ && "
               "/home/ubuntu/gladiatus-bot/venv/bin/python3 /home/ubuntu/gladiatus-bot/src/smelting.py "
               ">> /home/ubuntu/gladiatus-bot/logs/sell.log 2>&1")
    job = cron.new(command)
    job.hour.every(4)

    cron.write()
    await ctx.send("Done! Every 4 hours.")


@bot.command(name='inventory_smelt_stop')
async def inventory_smelt_stop(ctx):
    to_be_deleted = [crn for crn in cron if "smelt" in crn.command]
    for delete_cron in to_be_deleted:
        print(f"{delete_cron} removed!")
        cron.remove(delete_cron)
    cron.write()

# only once
@bot.command(name='inventory_smelt_once')
async def inventory_smelt_once(ctx):
    response = "Selling inventory process started. "
    await ctx.send(response)
    smelt = Smelt()

    smelt.calculate_smelt_status()

    # finish smelting
    smelt.take_resources_finished_smelting()

    # put items to smelt
    smelt.put_items_in_slots()

    await ctx.send("Smelted!")

# report
@bot.command(name='report')
async def report(ctx):
    response = "Selling inventory process started. "
    await ctx.send(response)
    d = BattleReport()
    db = GladiatusDB("players")

    db.create_table()
    reps = d.get_highest_rewards()
    for i in reps:
        # print(json.dumps(i, indent=4))
        db.insert_player(i)
    # res = db.query_players()
    # for j in res:
    #     print(json.dumps(j, indent=4))
    db.close()
    await ctx.send("Report done! Check database.")
    
bot.run(BOT_TOKEN)