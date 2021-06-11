import discord, os
from discord.ext import commands
from dotenv import load_dotenv
import json
from datetime import datetime
import calendar

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

cryptic_id = os.environ.get("CRYPTIC")
coding_id = os.environ.get("CODING")
lb_id = os.environ.get("LEADERBOARD_CHANNEL")

bot = commands.Bot(command_prefix=".", case_insensitive = True)
bot.remove_command('help')

########
#change weekly lb on monday 00:00 and print

@bot.event()
async def on_time():
    my_date = datetime.utcnow()
    day = calendar.day_name[my_date.weekday()]
    if "00:00:00" in my_date and day=="Monday":
        ch = bot.get_channel(lb_id)
        emb1 = discord.Embed(title = "Weekly Leaderboard", color = 0xFFD700)


########

@bot.command()
async def cryptic(ctx):
    emb = discord.Embed(title = "Cryptic Challenge", color = 0x800080)
    ch = bot.get_channel(cryptic_id)
    msg_content = ctx.message.content.strip(".cryptic ")
    emb.add_field(name = "Challenge", value = msg_content, inline = False)
    await ch.send(embed = emb)

@bot.command()
async def coding(ctx):
    emb = discord.Embed(title = "Coding Challenges", color = 0x800080)
    ch = bot.get_channel(coding_id)
    msg_content = ctx.message.content.strip(".coding ")
    emb.add_field(name = "Challenge", value = msg_content, inline=False)
    await ch.send(embed = emb)

@bot.command()
async def updatelb(ctx):
    msg = ctx.message.content.strip(".updatelb ")
    usr, code, crypt = msg.split()
    code = int(code)
    crypt = int(crypt)

    compltlb = {}
    with open("assets/complete_leaderboard.json", "r") as f:
        compltlb = json.load(f)
    f.close()

    if not compltlb:
        compltlb = {usr: {"code": code, "crypt": crypt}}
    else:
        if usr in compltlb:
            compltlb[usr]["code"]+=code
            compltlb[usr]["crypt"]+=crypt
        else:
            compltlb[usr] = {"code": code, "crypt": crypt}
    
    obj = json.dumps(compltlb, indent = 4)
    print(obj)
    with open("assets/complete_leaderboard.json", "w") as f:
        f.write(obj)
    f.close()

    wklylb = {}
    with open("assets/weekly_leaderboard.json", "r") as f:
        wklylb = json.load(f)
    f.close()
    if not wklylb:
        wklylb = {usr: {"code": code, "crypt": crypt}}
    else:
        if usr in wklylb:
            wklylb[usr]["code"]+=code
            wklylb[usr]["crypt"]+=crypt
        else:
            wklylb[usr] = {"code": code, "crypt": crypt}
    
    obj = json.dumps(wklylb, indent = 4)
    with open("assets/weekly_leaderboard.json", "w") as f:
        f.write(obj)
    f.close()
    

bot.run(TOKEN)