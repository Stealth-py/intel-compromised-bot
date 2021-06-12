import discord, os
from discord import user
from discord.ext import commands
from dotenv import load_dotenv
import json
from datetime import datetime
import calendar

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

cryptic_id = int(os.environ.get("CRYPTIC"))
coding_id = int(os.environ.get("CODING"))
lb_id = int(os.environ.get("LEADERBOARD_CHANNEL"))

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
        users, crypt, code = [], [], []
        total = []
        finalsc = []
        for usr in wkly:
            finalsc.append([usr, wkly[usr]["crypt"], wkly[usr]["code"], wkly[usr]["code"]+wkly[usr]["crypt"]])
        finalsc = sorted(finalsc, reverse = True, key = lambda x: x[3])
        c = 0
        for each in finalsc:
            if c==0:
                users.append(":first_place: "+each[0])
            elif c==1:
                users.append(":second_place: "+each[0])
            elif c==2:
                users.append(":third_place: "+each[0])
            crypt.append(each[1])
            code.append(each[2])
            total.append(each[3])
            c+=1

        tot = len(wkly)
        pages = tot//5 + 1
        if tot%5==0:
            pages-=1

        embs = []
        e1 = discord.Embed(title="Weekly Leaderboard", color = 0xFFD700)
        if c<=5:
            e1.add_field(name = "Username", value="\n".join(users), inline = True)
            e1.add_field(name = "Cryptic Score", value = "\n".join(crypt), inline = True)
            e1.add_field(name = "Comdimg Score", value = "\n".join(code), inline = True)
            e1.add_field(name = "Total Score", value = "\n".join(total), inline = True)
        else:
            e1.add_field(name = "Username", value="\n".join(users[:5]), inline = True)
            e1.add_field(name = "Cryptic Score", value = "\n".join(crypt[:5]), inline = True)
            e1.add_field(name = "Comdimg Score", value = "\n".join(code[:5]), inline = True)
            e1.add_field(name = "Total Score", value = "\n".join(total[:5]), inline = True)
        e1.set_footer(text = "Page 1", icon_url="https://cdn.discordapp.com/emojis/852073834337140756.png?v=1")
        e1.set_author(name = "Made with <3 by Stealth.py", url="https://github.com/Stealth-py/", icon_url="https://cdn.discordapp.com/avatars/389111703725539328/a_ad503cedb63402fa14d4b48e3e5e77ef.gif?size=256&f=.gif")
        embs.append(e1)
        i = 5
        for pg in range(2, pages+1):
            e = discord.Embed(title = "Weekly Leaderboard", color = 0xFFD700)
            if pg!=pages:
                e.add_field(name = "Username", value="\n".join(users[i:i+5]), inline = True)
                e.add_field(name = "Cryptic Score", value = "\n".join(crypt[i:i+5]), inline = True)
                e.add_field(name = "Comdimg Score", value = "\n".join(code[i:i+5]), inline = True)
                e.add_field(name = "Total Score", value = "\n".join(total[i:i+5]), inline = True)
            else:
                e.add_field(name = "Username", value="\n".join(users[i:]), inline = True)
                e.add_field(name = "Cryptic Score", value = "\n".join(crypt[i:]), inline = True)
                e.add_field(name = "Comdimg Score", value = "\n".join(code[i:]), inline = True)
                e.add_field(name = "Total Score", value = "\n".join(total[i:]), inline = True)
            e.set_footer(text = f"Page {pg}", icon_url="https://cdn.discordapp.com/emojis/852073834337140756.png?v=1")
            e.set_author(name = "Made with <3 by Stealth.py", url="https://github.com/Stealth-py/", icon_url="https://cdn.discordapp.com/avatars/389111703725539328/a_ad503cedb63402fa14d4b48e3e5e77ef.gif?size=256&f=.gif")
            embs.append(e)
            i+=5
########

@bot.command()
async def cryptic(ctx):
    emb = discord.Embed(title = "Cryptic Challenge", color = 0x800080)
    ch = bot.get_channel(cryptic_id)
    msg_content = ctx.message.content.strip(".cryptic ")
    emb.add_field(name = "Challenge", value = msg_content, inline = False)
    emb.set_footer(text="Good luck guys! <3")
    emb.set_thumbnail(url = "https://media1.tenor.com/images/d3f7680f8c32557237d41a1ea43854e5/tenor.gif?itemid=21381920")
    await ch.send(embed = emb)

@bot.command()
async def coding(ctx):
    emb = discord.Embed(title = "Coding Challenges", color = 0x800080)
    ch = bot.get_channel(coding_id)
    msg_content = ctx.message.content.strip(".coding ")
    emb.add_field(name = "Challenge", value = msg_content, inline=False)
    emb.set_footer(text="Good luck guys! <3")
    emb.set_thumbnail(url = "https://media1.tenor.com/images/d3f7680f8c32557237d41a1ea43854e5/tenor.gif?itemid=21381920")
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