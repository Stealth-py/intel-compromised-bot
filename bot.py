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

@bot.event
async def on_time():
    my_date = datetime.utcnow()
    day = calendar.day_name[my_date.weekday()]
    if "00:00:00" in my_date and day=="Monday":
        ch = bot.get_channel(lb_id)
        wkly = {}
        with open("assets/weekly_leaderboard.json", "r") as f:
            wkly = json.load(f)
        f.close()
        users = list(wkly.keys())
        crypt, code = [], []
        for usr in wkly:
            crypt.append(wkly[usr]["crypt"])
            code.append(wkly[usr]["code"])
        total = len(wkly)
        pages = total//5 + 1
        if total%5==0:
            pages-=1

        embs = []
        e1 = discord.Embed(title="Weekly Leaderboard", color = 0xFFD700)
        if len(users)<=5:
            e1.add_field(name = "Username", value="\n".join(users), inline = True)
            e1.add_field(name = "Cryptic Score", value = "\n".join(crypt), inline = True)
            e1.add_field(name = "Comdimg Score", value = "\n".join(code), inline = True)
        else:
            e1.add_field(name = "Username", value="\n".join(users[:5]), inline = True)
            e1.add_field(name = "Cryptic Score", value = "\n".join(crypt[:5]), inline = True)
            e1.add_field(name = "Comdimg Score", value = "\n".join(code[:5]), inline = True)
        e1.set_footer(text = "Page 1", icon_url="https://cdn.discordapp.com/emojis/852073834337140756.png?v=1")
        embs.append(e1)
        i = 5
        for pg in range(2, pages+1):
            e = discord.Embed(title = "")
            e.set_footer(text = f"Page {pg}", icon_url="https://cdn.discordapp.com/emojis/852073834337140756.png?v=1")
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