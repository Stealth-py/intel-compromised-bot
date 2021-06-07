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
    usr, cod, cr = msg.split()

    compltlb = {}
    with open("assets/complete_leaderboard.json", "r") as f:
        compltlb = json.load(f)
    f.close()

    wklylb = {}
    with open("assets/weekly_leaderboard", "r") as f:
        wklylb = json.load(f)
    f.close()

bot.run(TOKEN)