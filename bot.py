import discord, os
from discord import client
from discord.ext import commands, tasks
from discord.ext.commands import context
from dotenv import load_dotenv
import json
from datetime import date, datetime
import calendar

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

cryptic_id = int(os.environ.get("CRYPTIC"))
coding_id = int(os.environ.get("CODING"))
lb_id = int(os.environ.get("LEADERBOARD_CHANNEL"))

bot = commands.Bot(command_prefix=".", case_insensitive = True)
bot.remove_command('help')


@bot.command()
async def help(ctx):
    e1 = discord.Embed(title = "Help", color = 0xFFFFFF)
    try:
        if str(ctx.message.channel.category) == "Admin":
            e1.add_field(name = "answer", value = "Use this format to store the answer to the current cryptic hunt question.\n`.answer {put-your-answer-here}`\nFor example: `.answer seks` will put in the answer to the current question as `seks`.", inline = False)
        else:
            e1.add_field(name = "answer", value = "Format: `.answer {your-answer-to-the-question}`.\nUse this command to dm the bot with your answer to the current cryptic question. If the answer is correct, the points will be added.\nRemember, 10 points as each day passes, till the current level is open. So.. you know what to do don't you :).\nP.S.: PLEASE JUST DM THE BOT WITH THE ANSWER AND NOT USE THIS COMMAND ANYWHERE ELSE!", inline = False)
            e1.set_footer(text = "hmmm.", icon_url="https://cdn.discordapp.com/emojis/815651236162306078.png?v=1")
    except:
        e1.add_field(name = "hmm", value = "ok just use this command in the server you dumbo ._. fkn dumbass.. meh.")
        e1.set_thumbnail(url="https://media1.tenor.com/images/dd0935f96369c070cfba271ef0fce74a/tenor.gif?itemid=12516944")
        e1.set_footer(text = "ok well im a bit moody and not in a good mood rn. bring me a IMMIMMHNMHMMHMMHNNIMMINMINMHNM and bacon. i like that but with some vinegar on top, don't forget that.", icon_url="https://cdn.discordapp.com/emojis/845241476895866890.gif?v=1")
    await ctx.send(embed = e1)


@bot.command()
async def answer(ctx):
    if ctx.channel == bot.get_channel(770964768642433045):
        ans, pts = ctx.message.content.strip(".answer ")
        pts = int(pts)
        to_ans = {"answer": ans, "points": pts}
        with open("assets/answer.json", "r") as f:
            f.write(json.dumps(to_ans, indent=4))
        f.close()
    elif isinstance(ctx.channel, discord.channel.DMChannel):
        ans = ctx.message.content.strip(".answer ")
        ans = ''.join(ans.split()).lower()
        usr = ctx.message.author.name.lower()
        print(ans, type(usr))
        to_ans = {}
        with open("assets/answer.json", "r") as f:
            to_ans = json.load(f)
        f.close()
        if to_ans["answer"]==ans:
            crypt = int(to_ans["points"])
            compltlb = {}
            with open("assets/complete_leaderboard.json", "r") as f:
                compltlb = json.load(f)
            f.close()

            if not compltlb:
                compltlb = {usr: {"code": 0, "crypt": crypt}}
            else:
                if usr in compltlb:
                    compltlb[usr]["crypt"]+=crypt
                else:
                    compltlb[usr] = {"code": 0, "crypt": crypt}
            
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
                wklylb = {usr: {"code": 0, "crypt": crypt}}
            else:
                if usr in wklylb:
                    wklylb[usr]["crypt"]+=crypt
                else:
                    wklylb[usr] = {"code": 0, "crypt": crypt}
            obj = json.dumps(wklylb, indent = 4)
            print(obj)
            with open("assets/weekly_leaderboard.json", "w") as f:
                f.write(obj)
            f.close()

##update cryptic scores each day
@tasks.loop(seconds = 1.0)
async def decrement_score():
    my_date = datetime.now()
    day = my_date.weekday()
    if "00:00:00" in str(my_date):
        ans = {}
        with open("assets/answer.json", "r") as f:
            ans = json.load(f)
        f.close()
        if ans["complete"] == "false":
            ans["points"] -= 10*day
        obj = json.dumps(ans, indent=4)
        with open("assets/answer.json", "w") as f:
            f.write(obj)
        f.close()


decrement_score.start()



########
#change weekly lb on monday 00:00 and print

@tasks.loop(seconds = 1.0)
async def on_time():
    my_date = datetime.now()
    day = calendar.day_name[my_date.weekday()]
    my_date = str(my_date)
    day = str(day)
    # print(my_date, day)
    if "20:56:00" in my_date and day=="Wednesday":
        ch = bot.get_channel(lb_id)
        wkly = {}
        with open("assets/weekly_leaderboard.json", "r") as f:
            wkly = json.load(f)
        f.close()
        if wkly:
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
                else:
                    users.append(each[0])
                crypt.append(each[1])
                code.append(each[2])
                total.append(each[3])
                c+=1

            tot = len(wkly)
            pages = tot//5 + 1
            if tot%5==0:
                pages-=1
            
            wklylb = {}
            obj = json.dumps(wklylb, indent = 4)
            with open("assets/weekly_leaderboard.json", "w") as f:
                f.write(obj)
            f.close()

            embs = []
            e1 = discord.Embed(title="Weekly Leaderboard", color = 0xFFD700)
            if c<=5:
                e1.add_field(name = "Username", value="\n".join(map(str, users)), inline = True)
                e1.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt)), inline = True)
                e1.add_field(name = "Comdimg Score", value = "\n".join(map(str, code)), inline = True)
            else:
                e1.add_field(name = "Username", value="\n".join(map(str, users[:5])), inline = True)
                e1.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[:5])), inline = True)
                e1.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[:5])), inline = True)
            e1.set_footer(text = "Page 1", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
            embs.append(e1)
            i = 5
            for pg in range(1, pages):
                e = discord.Embed(title = "Weekly Leaderboard", color = 0xFFD700)
                if pg!=pages-1:
                    e.add_field(name = "Username", value="\n".join(map(str, users[i:i+5])), inline = True)
                    e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:i+5])), inline = True)
                    e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:i+5])), inline = True)
                else:
                    e.add_field(name = "Username", value="\n".join(map(str, users[i:])), inline = True)
                    e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:])), inline = True)
                    e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:])), inline = True)
                e.set_footer(text = f"Page {pg+1}", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
                embs.append(e)
                i+=5
            i = 0
            msg = await ch.send(embed = e1)
            await msg.add_reaction('⏮')
            await msg.add_reaction('◀')
            await msg.add_reaction('▶')
            await msg.add_reaction('⏭')
            print(embs, type(msg), pages, users)
            emoji = ''
            while 1:
                if emoji=="\u23ee":
                    i = 0
                    await msg.edit(embed = embs[i])
                if emoji == "\u25c0":
                    if i>0:
                        i-=1
                    await msg.edit(embed = embs[i])
                if emoji == "\u25b6":
                    if i<pages-1:
                        i+=1
                    await msg.edit(embed = embs[i])
                if emoji == "\u23ed":
                    i = pages-1
                    await msg.edit(embed = embs[i])
            
                flag, u = await bot.wait_for('reaction_add', check=lambda r, us: (r.emoji == '⏮' or r.emoji == '◀' or r.emoji == '▶' or r.emoji == '⏭' and r.message.id == msg.id) and msg.id == r.message.id and r.message.guild.id == msg.guild.id)
                if flag is None:
                    break
                if u.id != bot.user.id:
                    emoji = str(flag.emoji)
                    await msg.remove_reaction(flag.emoji, u)
            await msg.clear_reactions()
        else:
            e1 = discord.Embed(title="Weekly Leaderboard", color = 0xFFD700)
            e1.add_field(name = "No data yet!", value = "No users found. hmm. 13 bottles of vinegar and I'm compromised. You won't be disappointed, trust me. ;)", inline = False)
            e1.set_footer(text = "zW91OXb1tYLiCYIgNXH1wWOlGWOkeqmuyCEizS4=", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
            await ch.send(embed = e1)
        
########
on_time.start()
###

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
    usr, code = msg.split()
    code = int(code)

    usr = usr.lower()

    compltlb = {}
    with open("assets/complete_leaderboard.json", "r") as f:
        compltlb = json.load(f)
    f.close()

    if not compltlb:
        compltlb = {usr: {"code": code, "crypt": 0}}
    else:
        if usr in compltlb:
            compltlb[usr]["code"]+=code
        else:
            compltlb[usr] = {"code": code, "crypt": 0}
    
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
        wklylb = {usr: {"code": code, "crypt": 0}}
    else:
        if usr in wklylb:
            wklylb[usr]["code"]+=code
        else:
            wklylb[usr] = {"code": code, "crypt": 0}
    
    obj = json.dumps(wklylb, indent = 4)
    with open("assets/weekly_leaderboard.json", "w") as f:
        f.write(obj)
    f.close()

@bot.command()
async def showlb(ctx):
    ch = bot.get_channel(lb_id)
    wkly = {}
    with open("assets/weekly_leaderboard.json", "r") as f:
        wkly = json.load(f)
    f.close()
    if wkly:
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
            else:
                users.append(each[0])
            crypt.append(each[1])
            code.append(each[2])
            total.append(each[3])
            c+=1

        tot = len(wkly)
        pages = tot//5 + 1
        if tot%5==0:
            pages-=1
        
        wklylb = {}
        obj = json.dumps(wklylb, indent = 4)
        with open("assets/weekly_leaderboard.json", "w") as f:
            f.write(obj)
        f.close()

        embs = []
        e1 = discord.Embed(title="Weekly Leaderboard", color = 0xFFD700)
        if c<=5:
            e1.add_field(name = "Username", value="\n".join(map(str, users)), inline = True)
            e1.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt)), inline = True)
            e1.add_field(name = "Comdimg Score", value = "\n".join(map(str, code)), inline = True)
        else:
            e1.add_field(name = "Username", value="\n".join(map(str, users[:5])), inline = True)
            e1.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[:5])), inline = True)
            e1.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[:5])), inline = True)
        e1.set_footer(text = "Page 1", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
        embs.append(e1)
        i = 5
        for pg in range(1, pages):
            e = discord.Embed(title = "Weekly Leaderboard", color = 0xFFD700)
            if pg!=pages-1:
                e.add_field(name = "Username", value="\n".join(map(str, users[i:i+5])), inline = True)
                e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:i+5])), inline = True)
                e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:i+5])), inline = True)
            else:
                e.add_field(name = "Username", value="\n".join(map(str, users[i:])), inline = True)
                e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:])), inline = True)
                e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:])), inline = True)
            e.set_footer(text = f"Page {pg+1}", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
            embs.append(e)
            i+=5
        i = 0
        msg = await ch.send(embed = e1)
        await msg.add_reaction('⏮')
        await msg.add_reaction('◀')
        await msg.add_reaction('▶')
        await msg.add_reaction('⏭')
        print(embs, type(msg), pages, users)
        emoji = ''
        while 1:
            if emoji=="\u23ee":
                i = 0
                await msg.edit(embed = embs[i])
            if emoji == "\u25c0":
                if i>0:
                    i-=1
                await msg.edit(embed = embs[i])
            if emoji == "\u25b6":
                if i<pages-1:
                    i+=1
                await msg.edit(embed = embs[i])
            if emoji == "\u23ed":
                i = pages-1
                await msg.edit(embed = embs[i])
        
            flag, u = await bot.wait_for('reaction_add', check=lambda r, us: (r.emoji == '⏮' or r.emoji == '◀' or r.emoji == '▶' or r.emoji == '⏭' and r.message.id == msg.id) and msg.id == r.message.id and r.message.guild.id == msg.guild.id)
            if flag is None:
                break
            if u.id != bot.user.id:
                emoji = str(flag.emoji)
                await msg.remove_reaction(flag.emoji, u)
        await msg.clear_reactions()
    else:
        e1 = discord.Embed(title="Weekly Leaderboard", color = 0xFFD700)
        e1.add_field(name = "No data yet!", value = "No users found. hmm. 13 bottles of vinegar and I'm compromised. You won't be disappointed, trust me. ;)", inline = False)
        e1.set_footer(text = "zW91OXb1tYLiCYIgNXH1wWOlGWOkeqmuyCEizS4=", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
        await ch.send(embed = e1)

bot.run(TOKEN)