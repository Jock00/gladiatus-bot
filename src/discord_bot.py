import discord
from discord.ext import commands
from npc_attack import npc_attack
from dungeon_attack import DungeonAttack
from stats import Stats
from player_arena_attack import PlayerAttack
from auction import Auction
from crontab import CronTab 

guild_id = "1250688599318335610"

BOT_TOKEN = 'MTI1MDY4NzE3MDU4NzY2MDM1OQ.GmrPao.zIz4ZvPtDBo69bIIpcKDKAd72izOOwHhhSFAGc'


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
    commands = [
        "cd ../scripts",
        "sh player.sh"
        ]

    job=cron.new(command= (" && ").join(commands) + " >> ../logs/players.log 2>&1")
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
        await ctx.send(i)

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
    commands = [
        "cd ../scripts",
        "sh npc_attack.sh"
        ]

    job=cron.new(command= (" && ").join(commands) + " >> ../logs/npc.log 2>&1")
    job.minute.every(1) 
   
    cron.write()
    await ctx.send("Done")


@bot.command(name='attack_loop_npc_remove')
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
    commands = [
        "cd ../scripts",
        "sh dungeon_attack.sh"
        ]

    job=cron.new(command= (" && ").join(commands) + " >> ../logs/dungeon.log 2>&1")
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
    commands = [
        "cd ../scripts",
        "sh auction.sh"
        ]

    job=cron.new(command= (" && ").join(commands) + " >> ../logs/auction.log 2>&1")
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

bot.run(BOT_TOKEN)



