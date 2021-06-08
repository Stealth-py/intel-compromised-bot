import discord, os
from discord.ext import commands
from dotenv import load_dotenv
import json

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

cryptic_id = os.environ.get("CRYPTIC")
coding_id = os.environ.get("CODING")

bot = commands.Bot(command_prefix=".", case_insensitive = True)
bot.remove_command('help')

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

    print(usr, code, crypt)

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

    wklylb = {}
    with open("assets/weekly_leaderboard.json", "r") as f:
        wklylb = json.load(f)
    f.close()

    

bot.run(TOKEN)