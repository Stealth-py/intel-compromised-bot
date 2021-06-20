import discord, os
from discord import client
from discord import activity
from discord.channel import DMChannel
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
design_id = int(os.environ.get("DESIGN"))
gaming_id = int(os.environ.get("GAMING"))
lb_id = int(os.environ.get("LEADERBOARD_CHANNEL"))

act = discord.Game(name = ".help | hmm.")

bot = commands.Bot(command_prefix=".", case_insensitive = True, activity = act)
bot.remove_command('help')

@bot.command()
async def help(ctx):
    e1 = discord.Embed(title = "Help", color = 0xFFFFFF)
    try:
        if str(ctx.message.channel.category) == "Admin":
            e1.add_field(name = "`end`", value = "Use this command to mark an official end to the current week's challenges. This command will also stop accepting dm submissions for the cryptic challenge.", inline = False)
            e1.add_field(name = "`answer`", value = "Use this format to store the answer to the current cryptic hunt question.\nFormat: `.answer {put-your-answer-here}`\nFor example: `.answer seks` will put in the answer to the current question as `seks`.", inline = False)
            e1.add_field(name = "`updatelb`", value = "Format: `.updatelb {username-in-the-server} {coding-score} {design-score} {gaming-score}`.\nIf only one type of score is to be updated please use the others score(s) as 0. For example: If I need to update coding score for stealth.py by 100, type `.updatelb stealth.py 100 0 0`.", inline = False)
            e1.add_field(name = "`cryptic`", value = "Format: `.cryptic {the full challenge message}`.\nFor example: If the challenge message is, let's say, `decode frxf using ROT13`, then you need to type in the command `.cryptic decode frxf using ROT13`.", inline = False)
            e1.add_field(name = "`coding`", value = "Format: `.coding {the full challenge message}`.\nFor example: If the challenge message is, let's say, `make a discord bot which responds whenever a user writes hello in the chat`, then you need to type in the command `.coding make a discord bot which responds whenever a user writes hello in the chat`", inline = False)
            e1.add_field(name = "`design`", value = "Format: `.design {the full challenge message}`.\nFor example: If the challenge message is, let's say, `{some design related challenge here XD}`, then you need to type in the command `.design {some design related challenge here XD}`", inline = False)
            e1.add_field(name = "`gaming`", value = "Format: `.gaming {the full challenge message}`.\nFor example: If the challenge message is, let's say, `{some gaming related challenge here XD}`, then you need to type in the command `.gaming {some gaming related challenge here XD}`", inline = False)
        else:
            e1.add_field(name = "`answer`", value = "Format: `.answer {your-answer-to-the-question}`.\nUse this command to dm the bot with your answer to the current cryptic question. If the answer is correct, the points will be added.\nRemember, 10 points will be deducted as each day passes, till the current level is open. So.. you know what to do don't you :).\nP.S.: PLEASE JUST DM THE BOT WITH THE ANSWER AND NOT USE THIS COMMAND ANYWHERE ELSE!", inline = False)
        e1.add_field(name = "`showlb`", value = "Use this command to print out the current weekly leaderboard.", inline = False)
        e1.set_thumbnail(url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
        e1.set_footer(text = "hmmmk.", icon_url="https://cdn.discordapp.com/emojis/815651236162306078.png?v=1")
    except:
        e1.add_field(name = "hmm", value = "ok just use this command in the server you dumbass ._. bruh.. meh.")
        e1.set_thumbnail(url="https://media1.tenor.com/images/dd0935f96369c070cfba271ef0fce74a/tenor.gif?itemid=12516944")
        e1.set_footer(text = "ok well im a bit moody and not in a good mood rn. bring me a IMMIMMHNMHMMHMMHNNIMMINMINMHNM and bacon. i like that but with some vinegar on top, don't forget that.", icon_url="https://cdn.discordapp.com/emojis/845241476895866890.gif?v=1")
    await ctx.send(embed = e1)

@bot.command()
async def end(ctx, *args):
    e = discord.Embed(title = "Challenges have ended...", color = 0x4e5d94)
    ch = bot.get_channel(855843542428287006)
    if str(ctx.message.channel.category)=="Admin":
        ob = {}
        with open("assets/answer.json", "r") as f:
            ob = json.load(f)
        f.close()
        print(ob)
        ob["ongoing"] = False
        ob = json.dumps(ob, indent = 4)
        print(ob)
        with open("assets/answer.json", "w") as f:
            f.write(ob)
        f.close()
        e.add_field(name = "Good work guys :)", value = "@here This week's challenges have finally come to an end. Take some rest and wait for the judgement and new challenges, which would be starting off from Monday, next week. Obviously. ;)", inline = False)
        e.set_footer(text = "hmmk", icon_url="https://cdn.discordapp.com/emojis/815651236162306078.png?v=1")
        e.set_thumbnail(url = "https://i.giphy.com/media/SeysxkSfenHY4/giphy.gif")
        await ch.send(embed = e)
    else:
        e.add_field(name = "smarty", value = "how about a NO")
        e.set_thumbnail(url="https://i.gifer.com/Mw74.gif")
        await ctx.channel.send(embed = e)


@bot.command()
async def answer(ctx, *args):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        ans = ''.join(args)
        ans = ''.join(ans.split()).lower()
        usr = ctx.message.author.name.lower()
        print(ans, type(usr))
        to_ans = {}
        with open("assets/answer.json", "r") as f:
            to_ans = json.load(f)
        f.close()
        if to_ans["ongoing"] and to_ans["answer"]==ans and usr not in to_ans["completed"]:
            crypt = int(to_ans["points"])
            if to_ans["count"]==0:
                crypt+=1
            compltlb = {}
            with open("assets/complete_leaderboard.json", "r") as f:
                compltlb = json.load(f)
            f.close()

            if not compltlb:
                compltlb = {usr: {"code": 0, "crypt": crypt, "design": 0, "gaming": 0}}
            else:
                if usr in compltlb:
                    compltlb[usr]["crypt"]+=crypt
                else:
                    compltlb[usr] = {"code": 0, "crypt": crypt, "design": 0, "gaming": 0}

            obj = json.dumps(compltlb, indent = 4)
            with open("assets/complete_leaderboard.json", "w") as f:
                f.write(obj)
            f.close()

            wklylb = {}
            with open("assets/weekly_leaderboard.json", "r") as f:
                wklylb = json.load(f)
            f.close()
            if not wklylb:
                wklylb = {usr: {"code": 0, "crypt": crypt, "design": 0, "gaming": 0}}
            else:
                if usr in wklylb:
                    wklylb[usr]["crypt"]+=crypt
                else:
                    wklylb[usr] = {"code": 0, "crypt": crypt, "design": 0, "gaming": 0}
            obj = json.dumps(wklylb, indent = 4)
            print(obj)
            with open("assets/weekly_leaderboard.json", "w") as f:
                f.write(obj)
            f.close()
            
            to_ans["count"]+=1
            to_ans["completed"].append(usr)
            obj = json.dumps(to_ans, indent= 4)
            with open("assets/answer.json", "w") as f:
                f.write(obj)
            f.close()
            
            emb = discord.Embed(title = "Correct Answer :)", color=0xFFC0CB)
            emb.add_field(name = "Well done", value = "That answer is correct! Well done! Now, relax. Your points will be added to the points table.", inline = False)
            emb.set_thumbnail(url="https://media1.tenor.com/images/2386d12e54aa11ce0298d100954d982a/tenor.gif?itemid=4115606")
            await ctx.send(embed = emb)

    elif str(ctx.message.channel.category) == "Admin":
        ans = ''.join(args).lower()
        to_ans = {"answer": ans, "points": 100, "count": 0, "completed": [], "ongoing": True}
        obj = json.dumps(to_ans, indent=4)
        with open("assets/answer.json", "w") as f:
            f.write(obj)
        f.close()
        print(to_ans)
    else:
        emb = discord.Embed(title="OMFG", color=0xff0000)
        emb.set_thumbnail(url = "https://cdn.discordapp.com/emojis/690588303384248370.png?v=1")
        emb.add_field(name="BRO!", value="I TOLD YOU TO NOT USE THIS COMMAND ANYWHERE ELSE DIDNT I? YOU FKN DUMBASS...")
        emb.set_footer(text="hmmm. no. 😡", icon_url="https://cdn.discordapp.com/emojis/802002531487973396.gif?v=1")
        await ctx.message.author.send(embed=emb)
        await ctx.message.delete()

##update cryptic scores each day
@tasks.loop(seconds = 1.0)
async def decrement_score():
    my_date = datetime.now()
    day = my_date.weekday()
    if "00:00:00" in str(my_date):
        ch = bot.get_channel(782719007664242741)
        ans = {}
        with open("assets/answer.json", "r") as f:
            ans = json.load(f)
        f.close()
        if ans["ongoing"] == True:
            ans["points"] -= 10*day
        obj = json.dumps(ans, indent=4)
        with open("assets/answer.json", "w") as f:
            f.write(obj)
        f.close()
        await ch.send("Score has decreased by 10 points.")


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
    if "00:00:00" in my_date and day=="Monday":
        ch = bot.get_channel(lb_id)
        wkly = {}
        with open("assets/weekly_leaderboard.json", "r") as f:
            wkly = json.load(f)
        f.close()
        if wkly:
            users, crypt, code = [], [], []
            design, gaming = [], []
            total = []
            finalsc = []
            for usr in wkly:
                finalsc.append([usr, wkly[usr]["crypt"], wkly[usr]["code"], wkly[usr]["code"]+wkly[usr]["crypt"]+wkly[usr]["design"]+wkly[usr]["gaming"], wkly[usr]["design"], wkly[usr]["gaming"]])
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
                design.append(each[4])
                gaming.append(each[5])
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
                e1.add_field(name = "Design Score", value = "\n".join(map(str, design)), inline = True)
                e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming)), inline = True)
            else:
                e1.add_field(name = "Username", value="\n".join(map(str, users[:5])), inline = True)
                e1.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[:5])), inline = True)
                e1.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[:5])), inline = True)
                e1.add_field(name = "Design Score", value = "\n".join(map(str, design[:5])), inline = True)
                e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming[:5])), inline = True)
            e1.set_footer(text = "Page 1", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
            embs.append(e1)
            i = 5
            for pg in range(1, pages):
                e = discord.Embed(title = "Weekly Leaderboard", color = 0xFFD700)
                if pg!=pages-1:
                    e.add_field(name = "Username", value="\n".join(map(str, users[i:i+5])), inline = True)
                    e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:i+5])), inline = True)
                    e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:i+5])), inline = True)
                    e1.add_field(name = "Design Score", value = "\n".join(map(str, design[i:i+5])), inline = True)
                    e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming[i:i+5])), inline = True)
                else:
                    e.add_field(name = "Username", value="\n".join(map(str, users[i:])), inline = True)
                    e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:])), inline = True)
                    e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:])), inline = True)
                    e1.add_field(name = "Design Score", value = "\n".join(map(str, design[i:])), inline = True)
                    e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming[i:])), inline = True)
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
async def cryptic(ctx, *args):
    emb = discord.Embed(title = "Cryptic Challenge", color = 0x800080)
    ch = bot.get_channel(cryptic_id)
    msg_content = ' '.join(args)
    emb.add_field(name = "Challenge", value = msg_content, inline = False)
    emb.set_footer(text="Good luck guys! <3")
    emb.set_thumbnail(url = "https://media1.tenor.com/images/d3f7680f8c32557237d41a1ea43854e5/tenor.gif?itemid=21381920")
    await ch.send(embed = emb)

@bot.command()
async def coding(ctx, *args):
    emb = discord.Embed(title = "Coding Challenges", color = 0x800080)
    ch = bot.get_channel(coding_id)
    msg_content = ' '.join(args)
    emb.add_field(name = "Challenge", value = msg_content, inline=False)
    emb.set_footer(text="Good luck guys! <3")
    emb.set_thumbnail(url = "https://media1.tenor.com/images/d3f7680f8c32557237d41a1ea43854e5/tenor.gif?itemid=21381920")
    await ch.send(embed = emb)

@bot.command()
async def design(ctx, *args):
    emb = discord.Embed(title = "Design Challenges", color = 0x800080)
    ch = bot.get_channel(design_id)
    msg_content = ' '.join(args)
    emb.add_field(name = "Challenge", value = msg_content, inline=False)
    emb.set_footer(text="Good luck guys! <3")
    emb.set_thumbnail(url = "https://media1.tenor.com/images/d3f7680f8c32557237d41a1ea43854e5/tenor.gif?itemid=21381920")
    await ch.send(embed = emb)

@bot.command()
async def gaming(ctx, *args):
    emb = discord.Embed(title = "Gaming Challenges", color = 0x800080)
    ch = bot.get_channel(coding_id)
    msg_content = ' '.join(args)
    emb.add_field(name = "Challenge", value = msg_content, inline=False)
    emb.set_footer(text="Good luck guys! <3")
    emb.set_thumbnail(url = "https://media1.tenor.com/images/d3f7680f8c32557237d41a1ea43854e5/tenor.gif?itemid=21381920")
    await ch.send(embed = emb)

@bot.command()
async def updatelb(ctx, *args):
    usr, code, des, gam = args[0], args[1], args[2], args[3]
    code = int(code)
    des = int(des)
    gam = int(gam)

    usr = usr.lower()

    compltlb = {}
    with open("assets/complete_leaderboard.json", "r") as f:
        compltlb = json.load(f)
    f.close()

    if not compltlb:
        compltlb = {usr: {"code": code, "crypt": 0, "design": des, "gaming": gam}}
    else:
        if usr in compltlb:
            compltlb[usr]["code"]+=code
            compltlb[usr]["design"]+=des
            compltlb[usr]["gaming"]+=gam
        else:
            compltlb[usr] = {"code": code, "crypt": 0, "design": des, "gaming": gam}
    
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
        wklylb = {usr: {"code": code, "crypt": 0, "design": des, "gaming": gam}}
    else:
        if usr in wklylb:
            wklylb[usr]["code"]+=code
            wklylb[usr]["design"]+=des
            wklylb[usr]["gaming"]+=gam
        else:
            wklylb[usr] = {"code": code, "crypt": 0, "design": des, "gaming": gam}
    
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
        design, gaming = [], []
        total = []
        finalsc = []
        for usr in wkly:
            finalsc.append([usr, wkly[usr]["crypt"], wkly[usr]["code"], wkly[usr]["code"]+wkly[usr]["crypt"]+wkly[usr]["design"]+wkly[usr]["gaming"], wkly[usr]["design"], wkly[usr]["gaming"]])
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
            design.append(each[4])
            gaming.append(each[5])
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
            e1.add_field(name = "Design Score", value = "\n".join(map(str, design)), inline = True)
            e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming)), inline = True)
        else:
            e1.add_field(name = "Username", value="\n".join(map(str, users[:5])), inline = True)
            e1.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[:5])), inline = True)
            e1.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[:5])), inline = True)
            e1.add_field(name = "Design Score", value = "\n".join(map(str, design[:5])), inline = True)
            e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming[:5])), inline = True)
        e1.set_footer(text = "Page 1", icon_url="https://cdn.discordapp.com/emojis/853313275160035348.gif?v=1")
        embs.append(e1)
        i = 5
        for pg in range(1, pages):
            e = discord.Embed(title = "Weekly Leaderboard", color = 0xFFD700)
            if pg!=pages-1:
                e.add_field(name = "Username", value="\n".join(map(str, users[i:i+5])), inline = True)
                e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:i+5])), inline = True)
                e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:i+5])), inline = True)
                e1.add_field(name = "Design Score", value = "\n".join(map(str, design[i:i+5])), inline = True)
                e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming[i:i+5])), inline = True)
            else:
                e.add_field(name = "Username", value="\n".join(map(str, users[i:])), inline = True)
                e.add_field(name = "Cryptic Score", value = "\n".join(map(str, crypt[i:])), inline = True)
                e.add_field(name = "Comdimg Score", value = "\n".join(map(str, code[i:])), inline = True)
                e1.add_field(name = "Design Score", value = "\n".join(map(str, design[i:])), inline = True)
                e1.add_field(name = "Gaming Score", value = "\n".join(map(str, gaming[i:])), inline = True)
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