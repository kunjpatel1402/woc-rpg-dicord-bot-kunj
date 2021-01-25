import discord
from discord.ext import commands
import random
from characters.classes import person
from characters.classes import _member
from characters.classes import team
from characters.classes import teamplayer
import json
import os

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '/',intents=intents)

#emoji
crossed_swords=':crossed_swords:'
man_running=':man_running:'
wizard=":man_mage:"
bow_arrow=":bow_and_arrow:"
armour=":mechanical_arm:"

# variables
name = ''
running=True
members=[]
multi_players=[]
json_data=[]
single_players=[]
single_opponents=[]
teams=[]
team_players=[]

#setup-------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    print(f"{member} joined")
    
@client.event
async def on_member_remove(member):
    print(f"{member}left")


@client.event
async def on_ready():
    global json_data
    global members
    try:
        with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
            json_data=json.load(file)
            for item in json_data:
                temp_member=_member(item["name"],item["id"],item["xp"],item["hp"],item["dmg"],item["hp_level"],item["dmg_level"])
                print("name",temp_member.get_member_name())
                print("id",temp_member.get_id())
                members.append(temp_member)
            print(members)
            print(json_data)
            file.close()
        print('bot ready')
    except:
        with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","w") as file:
            file.write("[]")
            file.close()
        print('bot ready')

@client.command()
async def create_profile(ctx):
    global json_data
    global members
    print(members)
    flag=1
    for item in members:
        print("here")
        print(item.get_id())
        print(ctx.message.author.id)
        if item.get_id()==int(ctx.message.author.id):
            flag=0
            await ctx.send("profile already exists")
        print("end")
    if flag:
        _person=_member(ctx.message.author.name+'#'+ctx.message.author.discriminator,ctx.message.author.id,0,100,20,0,0)
        temp_data={"name":ctx.message.author.name+'#'+ctx.message.author.discriminator,"id":ctx.message.author.id,"xp":0,"hp":100,"dmg":20,"hp_level":0,"dmg_level":0,"status":"free"}
        json_data.append(temp_data)
        members.append(_person)
        print(members)
        print(json_data)
        with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
            file.seek(0)
            file.write(json.dumps(json_data))
            file.close()
            print(f"created {ctx.message.author}")

@client.command()
async def commands(ctx):
    await ctx.send("/start to start single player mode")
    await ctx.send("/create_profile creates profile in database")
    await ctx.send("/spawn to spawn in multiplayer battle")
    await ctx.send("/duel to attack in multi player battle")
    await ctx.send("/rage to do extensive damage in multi player battle")
    await ctx.send("/attack to attack goblin in single player mode")
    await ctx.send("/evade to evade in single player mode")
    await ctx.send("/exit_single_player to exit single player mode")
    await ctx.send("/exit_multi_player to exit multiplayer mode")
    await ctx.send("/list to get list of players in mulyiplayer mode")


@client.command()
async def shop(ctx):
    await ctx.send("upgrades available:")
    await ctx.send("1. type /hp to increase hp level")
    await ctx.send("1. type /dmg to increase damage level")

@client.command()
async def hp(ctx):
    flag=1
    for item in json_data:
        if int(item["id"])==int(ctx.message.author.id):
            level=item["hp_level"]
            cost=50*pow(1.5,level+1)
            new_hp=item["hp"]+(item["hp"]*0.67)
            if cost <= item["xp"]:
                await ctx.send("increasing hp level")
                item["hp_level"]+=1
                item["xp"]=item["xp"]-cost
                await ctx.send(f"{cost} deducted from xp")
                item["hp"]=new_hp
                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                    file.truncate(0)
                    file.seek(0)
                    file.write(json.dumps(json_data))
                    file.close()
                for profile in members:
                    if int(profile.get_id())==int(ctx.message.author.id):
                        updated_member=_member(profile.get_member_name(),profile.get_id(),item["xp"],item["hp"],item["dmg"],item["hp_level"],item["dmg_level"])
                        members.remove(profile)
                        members.append(updated_member)
                        print("updated hp")
                        flag=0
                        break
            else:
                await ctx.send("insufficient xp")
                flag=0
            break
    if flag:
        await ctx.send("profile not made")

@client.command()
async def dmg(ctx):
    flag=1
    for item in json_data:
        if int(item["id"])==int(ctx.message.author.id):
            level=item["dmg_level"]
            cost=50*pow(1.5,level+1)
            new_dmg=item["dmg"]+(item["dmg"]*0.67)
            if cost <= item["xp"]:
                await ctx.send("increasing damage level")
                item["dmg_level"]+=1
                item["xp"]=item["xp"]-cost
                await ctx.send(f"{cost} deducted from xp")
                item["dmg"]=new_dmg
                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                    file.truncate(0)
                    file.seek(0)
                    file.write(json.dumps(json_data))
                    file.close()
                for profile in members:
                    if int(profile.get_id())==int(ctx.message.author.id):
                        updated_member=_member(profile.get_member_name(),profile.get_id(),item["xp"],item["hp"],item["dmg"],item["hp_level"],item["dmg_level"])
                        members.remove(profile)
                        members.append(updated_member)
                        print("updated hp")
                        flag=0
                        break
            else:
                await ctx.send("insufficient xp")
                flag=0
            break
    if flag:
        await ctx.send("profile not made")

@client.command()
async def show_profile(ctx):
    check=1
    for item in members:
        if int(ctx.message.author.id)==int(item.get_id()):
            await ctx.send(f"max hp:{item.get_member_max_hp()}")
            await ctx.send(f"damage:{item.get_member_damage()}")
            await ctx.send(f"name:{item.get_member_name()}")
            await ctx.send(f"xp:{item.get_member_xp()}")
            await ctx.send(f"hp level:{item.get_member_hp_level()}")
            await ctx.send(f"damage level:{item.get_member_damage_level()}")
            check=0
            break
    if check:
        await ctx.send("profile not found")


#single player-----------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command()
async def start(ctx):
    await ctx.send(f'Choose a class\n1.{armour}Warrior \n2.{bow_arrow}Archer \n3.{":man_mage:"}Wizard')

@client.command()
async def warrior(ctx):
    flag=0
    name=ctx.message.author.name+'#'+ctx.message.author.discriminator
    for member in members:
        print(name)
        print(member.name)
        if name == member.name:
            print("flag1")
            flag=1
            xp=member.get_member_xp()
    if flag:
        for item in json_data:
            if str(item["id"])==str(ctx.message.author.id):
                if item["status"]=="free":
                    soldier=person(100,xp,name,20,ctx.message.author.id,"single")
                    single_players.append(soldier)
                    goblin=person(150,0,"GOBLIN",10,ctx.message.author.id,"single")
                    single_opponents.append(goblin)
                    await ctx.send(f'Welcome!! Brave heart')
                    await ctx.send("TYPE proceed TO CONTINUE")
                    item["status"]="single"
                    with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                        file.truncate(0)
                        file.seek(0)
                        file.write(json.dumps(json_data))
                        file.close()
                else:
                    await ctx.send("you are not playing single player mode")
    else:
        await ctx.send("please create a profile by typing /create_profile")
@client.command()
async def archer(ctx):
    flag=0
    name=ctx.message.author.name+'#'+ctx.message.author.discriminator
    for member in members:
        print(name)
        print(member.name)
        if name == member.name:
            print("flag1")
            flag=1
            xp=member.get_member_xp()
    if flag:
        for item in json_data:
            if str(item["id"])==str(ctx.message.author.id):
                if item["status"]=="free":
                    soldier=person(80,xp,name,25,ctx.message.author.id,"single")
                    single_players.append(soldier)
                    goblin=person(150,0,"GOBLIN",10,ctx.message.author.id,"single")
                    single_opponents.append(goblin)
                    await ctx.send(f'Welcome!! Brave heart')
                    await ctx.send("TYPE proceed TO CONTINUE")
                    item["status"]="single"
                    with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                        file.truncate(0)
                        file.seek(0)
                        file.write(json.dumps(json_data))
                        file.close()
                else:
                    await ctx.send("you are not playing single player mode")
    else:
        await ctx.send("please create a profile by typing /create_profile")
@client.command()
async def wizard(ctx):
    flag=0
    name=ctx.message.author.name+'#'+ctx.message.author.discriminator
    for member in members:
        print(name)
        print(member.name)
        if name == member.name:
            print("flag1")
            flag=1
            xp=member.get_member_xp()
    if flag:
        for item in json_data:
            print("inside for")
            if str(item["id"])==str(ctx.message.author.id):
                print("checked id")
                if str(item["status"])=="free":
                    print("player free")
                    soldier=person(60,xp,name,30,ctx.message.author.id,"single")
                    single_players.append(soldier)
                    goblin=person(150,0,"GOBLIN",10,ctx.message.author.id,"single")
                    single_opponents.append(goblin)
                    await ctx.send(f'Welcome!! Brave heart')
                    await ctx.send("TYPE proceed TO CONTINUE")
                    item["status"]="single"
                    print("player single")
                    with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                        file.truncate(0)
                        file.seek(0)
                        file.write(json.dumps(json_data))
                        file.close()
                else:
                    await ctx.send("you are not playing single player mode")
    else:
        await ctx.send("please create a profile by typing /create_profile")

@client.command()
async def proceed(ctx):
    await ctx.send("YOU WERE TRAVELLING THROUGH WOODS AND SUDDENLY A GOBLIN APPEARED")
    await ctx.send(f"WHAT WILL YOU LIKE TO DO:\n1. {crossed_swords}attack\n2. {man_running}evade")

@client.command()
async def attack(ctx):
    flag=1
    for player in single_players:
        if str(player.get_id())==str(ctx.message.author.id):
            for enemy in single_opponents:
                if str(enemy.get_id())==str(player.get_id()):
                    dmg=player.generate_damage()
                    enemy.take_damage(dmg)
                    await ctx.send(f"{player.get_name()} attacked attack for {dmg} hp")
                    dmg=enemy.generate_damage()
                    player.take_damage(dmg)
                    await ctx.send(f"goblin attacked {player.get_name()} for {dmg} hp")
                    flag=0
                    if enemy.get_hp()<=0:
                        await ctx.send(f"{player.get_name()} you win ")
                        await ctx.send(f"{player.get_name()} you are awarded 5 xp ")
                        for item in json_data:
                            if str(item["name"])==str(player.get_name()):
                                item["xp"]+=5
                                item["status"]="free"
                                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                    file.truncate(0)
                                    file.seek(0)
                                    file.write(json.dumps(json_data))
                                    file.close()
                                break
                        single_opponents.remove(goblin)
                        single_players.remove(player)
                    elif player.get_hp()<=0:
                        await ctx.send(f"{player.get_name()} you lose!!")
                        for item in json_data:
                            if str(item["name"])==str(player.get_name()):
                                item["status"]="free"
                                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                    file.truncate(0)
                                    file.seek(0)
                                    file.write(json.dumps(json_data))
                                    file.close()
                                break
                        single_opponents.remove(enemy)
                        single_players.remove(player)
                    else:
                        await ctx.send("choose you next move")
                    break
        if flag==0:
            break
    if flag:
        await ctx.send("you are not playing single player mode")



@client.command()
async def evade(ctx):
    flag=1
    for player in single_players:
        if str(player.get_id())==str(ctx.message.author.id):
            for enemy in single_opponents:
                if str(enemy.get_id())==str(player.get_id()):
                    dmg=5
                    player.take_damage(dmg)
                    await ctx.send(f"goblin attacked {player.get_name()} for {dmg} hp")
                    flag=0
                    if player.get_hp()<=0:
                        await ctx.send(f"{player.get_name()} you lose!!")
                        for item in json_data:
                            if str(item["name"])==str(player.get_name()):
                                item["status"]="free"
                                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                    file.truncate(0)
                                    file.seek(0)
                                    file.write(json.dumps(json_data))
                                    file.close()
                                break
                        single_opponents.remove(enemy)
                        single_players.remove(player)
                    else:
                        await ctx.send("choose you next move")
                    break
        if flag==0:
            break
    if flag:
        await ctx.send("you are not playing single player mode")

@client.command()
async def exit_single_player(ctx):
    flag=1
    for data in json_data:
        if data["id"]==ctx.message.author.id:
            if data["status"]=="single":
                data["status"]="free"
                for player in single_players:
                    if player.get_id()==ctx.message.author.id:
                        single_players.remove(player)
                        await ctx.send(f"{player.get_name()} exits single player mode")
                        break
                for player in single_opponents:
                    if player.get_id()==ctx.message.author.id:
                        single_opponents.remove(player)
                        break
                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                    file.truncate(0)
                    file.seek(0)
                    file.write(json.dumps(json_data))
                    file.close()
                flag=0
                break
    if flag:
        await ctx.send("you are not in single player mode")


#multiplayer-------------------------------------------------------------------------------------------------------------------------------------------------------------
member_damage=0
member_max_hp=0

@client.command()
async def ping(ctx):
    emoji = '\N{THUMBS UP SIGN}'
    await ctx.send(emoji)

@client.command()
async def clear(ctx,amount=10):
    await ctx.channel.purge(limit=amount)

@client.command(aliases=['list'])
async def _list(ctx):
    print("here")
    global multi_players
    print(multi_players)
    flag=1
    for player in multi_players:
        print("listing")
        await ctx.send(f"name:{player.get_name()}")
        await ctx.send(f"hp:{player.get_hp()}")
        await ctx.send(f"xp:{player.get_xp()}")
        flag=0
    if flag:
        await ctx.send("no players have spawned yet")

@client.command(aliases=['duel'])
async def attack_1(ctx,member):
    num=random.randint(1,10)
    global multi_players
    attacker=person(0,0,0,0,0,"xyz")
    print(attacker.get_damage())
    item=person(0,0,0,0,0,0)
    for item in multi_players:
        if int(item.get_id())==int(ctx.message.author.id):
            attacker=person(item.get_maxhp(),item.get_xp(),item.get_name(),item.get_damage(),item.get_id(),item.get_status())
            print("attacker found")
            break
    if str(item.get_status())=="multi":
        if attacker.get_damage()==0:
            await ctx.send("you have not spawned yet")
        elif attacker.get_damage():
            flag=1
            member_id=''
            j=3
            while(member[j]!='>'):
                member_id=(member_id+member[j])
                j+=1
            print("here")
            print(multi_players)
            print(member_id)
            print(ctx.message.author.id)
            if int(member_id)==int(ctx.message.author.id):
                await ctx.send("you cannot attack yourself ")
            else:
                for player in multi_players:
                    print("inside for loop")
                    print(player.get_id())
                    print(member_id)
                    if player.get_id()==int(member_id):
                        flag=0
                        if num>=1 and num<=7:
                            dmg=attacker.generate_damage()
                            print(dmg)
                            print(attacker.get_damage())
                            player.take_damage(dmg)
                            await ctx.send(f"{attacker.get_name()} attacked {player.get_name()} for {dmg} hp")
                            if player.get_hp()<=0:
                                await ctx.send(f'{player.get_name()} you lose')
                                for item in json_data:
                                    if item["name"]==ctx.message.author.name+'#'+ctx.message.author.discriminator:
                                        item["xp"]+=10
                                        await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} have been awarded 10 xp")
                                    if (item["name"])==str(player.get_name()):
                                        item["status"]="free"
                                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                    file.truncate(0)
                                    file.seek(0)
                                    file.write(json.dumps(json_data))
                                    file.close()
                                multi_players.remove(player)
                            break
                        else:
                            await ctx.send(f"{attacker.get_name()} missed his attack on {player.get_name()}")
                            break
                if flag:
                    await ctx.send("no such player found or player dead")                    
    else:
        await ctx.send("you are currently not playing multi player mode cannot execute this command")


@client.command(aliases=['rage'])
async def rageattack(ctx,member):
    global multi_players
    attacker=person(0,0,0,0,0,"xyz")
    print(attacker.get_damage())
    item=person(0,0,0,0,0,0)
    for item in multi_players:
        if int(item.get_id())==int(ctx.message.author.id):
            attacker=person(item.get_maxhp(),item.get_xp(),item.get_name(),item.get_damage(),item.get_id(),item.get_status())
            print("attacker found")
            break
    if str(item.get_status())=="multi":
        if attacker.get_damage()==0:
            await ctx.send("you have not spawned yet")
        elif attacker.get_damage():
            flag=1
            member_id=''
            j=3
            while(member[j]!='>'):
                member_id=(member_id+member[j])
                j+=1
            print("here")
            print(multi_players)
            print(member_id)
            print(ctx.message.author.id)
            if int(member_id)==int(ctx.message.author.id):
                await ctx.send("you cannot attack yourself ")
            else:
                for player in multi_players:
                    print("inside for loop")
                    print(player.get_id())
                    print(member_id)
                    if int(player.get_id())==int(member_id):
                        print("id verified")
                        print(player.get_xp())
                        if int(attacker.get_xp())>=5:
                            print("xp checked",player.get_xp())
                            item.reduce_xp(5)
                            print("xp",attacker.get_xp())
                            for item in json_data:
                                if item["id"]==attacker.get_id():
                                    item["xp"]-=5
                            with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                file.truncate(0)
                                file.seek(0)
                                file.write(json.dumps(json_data))
                                file.close()
                            await ctx.send("5 xp deducted")
                            dmg=attacker.generate_damage()
                            print(dmg+10)
                            print(attacker.get_damage())
                            player.take_damage(dmg+10)
                            flag=0
                            await ctx.send(f"{attacker.get_name()} attacked extensively {player.get_name()}")
                        else:
                            await ctx.send("insufficient xp")
                            flag=0
                        if player.get_hp()<=0:
                            await ctx.send(f'{player.get_name()} you lose')
                            for item in json_data:
                                if item["name"]==ctx.message.author.name+'#'+ctx.message.author.discriminator:
                                    item["xp"]+=10
                                    await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} have been awarded 10 xp")
                                if (item["name"])==str(player.get_name()):
                                    item["status"]="free"
                            with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                file.truncate(0)
                                file.seek(0)
                                file.write(json.dumps(json_data))
                                file.close()
                            multi_players.remove(player)
                            break
                if flag:
                    await ctx.send("no such player found or player dead")
    else:
        await ctx.send("you are currently not playing multi player mode cannot execute this command")


@client.command(aliases=['heal'])
async def heal_yourself(ctx,member):
    global multi_players
    healer=person(0,0,0,0,0,"xyz")
    print(healer.get_damage())
    item=person(0,0,0,0,0,0)
    for item in multi_players:
        if int(item.get_id())==int(ctx.message.author.id):
            healer=person(item.get_maxhp(),item.get_xp(),item.get_name(),item.get_damage(),item.get_id(),item.get_status())
            print("healer found")
            break
    if str(item.get_status())=="multi":
        if healer.get_damage()==0:
            await ctx.send("you have not spawned yet")
        elif healer.get_damage():
            flag=1
            member_id=''
            j=3
            while(member[j]!='>'):
                member_id=(member_id+member[j])
                j+=1
            print("here")
            print(multi_players)
            print(member_id)
            print(ctx.message.author.id)
            for player in multi_players:
                print("inside for loop")
                print(player.get_id())
                print(member_id)
                if int(player.get_id())==int(member_id):
                    print("id verified")
                    print(player.get_xp())
                    if int(healer.get_xp())>=8:
                        print("xp checked",player.get_xp())
                        item.reduce_xp(8)
                        print("xp",healer.get_xp())
                        for item in json_data:
                            if item["id"]==healer.get_id():
                                item["xp"]-=8
                        with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                            file.truncate(0)
                            file.seek(0)
                            file.write(json.dumps(json_data))
                            file.close()
                        await ctx.send("8 xp deducted")
                        print(healer.get_damage())
                        player.take_damage(-player.get_maxhp())
                        flag=0
                        await ctx.send(f"{healer.get_name()} healed {player.get_name()}")
                    else:
                        await ctx.send("insufficient xp")
                        flag=0
                    if player.get_hp()<=0:
                        await ctx.send(f'{player.get_name()} you lose')
                        for item in json_data:
                            if item["name"]==ctx.message.author.name+'#'+ctx.message.author.discriminator:
                                item["xp"]+=10
                                await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} have been awarded 10 xp")
                            if (item["name"])==str(player.get_name()):
                                item["status"]="free"
                        with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                            file.truncate(0)
                            file.seek(0)
                            file.write(json.dumps(json_data))
                            file.close()
                        multi_players.remove(player)
                        break
            if flag:
                await ctx.send("no such player found or player dead")
    else:
        await ctx.send("you are currently not playing multi player mode cannot execute this command")

@client.command()
async def spawn(ctx):
    var=1
    if var:
        global multi_players
        global members
        check=1
        for player in multi_players:
            if player.get_id()==ctx.message.author.id:
                check=0
        if check:
            flag=1
            for item in members:
                if item.get_id()==int(ctx.message.author.id):
                    new_person=person(item.get_member_max_hp(),item.get_member_xp(),item.get_member_name(),item.get_member_damage(),ctx.message.author.id,"multi")
                    for data in json_data:
                        if int(data["id"])==int(item.get_id()):
                            if data["status"]=="free":
                                data["status"]="multi"
                                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                    file.truncate(0)
                                    file.seek(0)
                                    file.write(json.dumps(json_data))
                                    file.close()
                                multi_players.append(new_person)
                                await ctx.send(f"{item.get_member_name()} spawned in multi player mode")
                            else:
                                await ctx.send("cannot execute this command in this mode")
                    flag=0
            if flag:
                await ctx.send("profile not found create one with /create_profile")
            print(multi_players)
        elif check==0:
            await ctx.send("player already spawned")
    else:
        await ctx.send("you are not playing multiplayer mode")

@client.command()
async def exit_multi_player(ctx):
    flag=1
    for data in json_data:
        if data["id"]==ctx.message.author.id:
            if data["status"]=="multi":
                data["status"]="free"
                for player in multi_players:
                    if player.get_id()==ctx.message.author.id:
                        multi_players.remove(player)
                        await ctx.send(f"{player.get_name()} exits multi player mode")
                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                    file.truncate(0)
                    file.seek(0)
                    file.write(json.dumps(json_data))
                    file.close()
                flag=0
                break
    if flag:
        await ctx.send("you are not in multi player mode")

#team player-------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command()
async def spawn_team_mode(ctx):
    var=1
    if var:
        global team_players
        global members
        check=1
        for player in team_players:
            if player.get_id()==ctx.message.author.id:
                check=0
        if check:
            flag=1
            for item in members:
                if item.get_id()==int(ctx.message.author.id):
                    new_person=teamplayer(item.get_member_max_hp(),item.get_member_xp(),item.get_member_name(),item.get_member_damage(),ctx.message.author.id,"team")
                    team_players.append(new_person)
                    for data in json_data:
                        if int(data["id"])==int(item.get_id()):
                            if data["status"]=="free":
                                data["status"]="team"
                                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                    file.truncate(0)
                                    file.seek(0)
                                    file.write(json.dumps(json_data))
                                    file.close()
                                multi_players.append(new_person)
                                await ctx.send(f"{item.get_member_name()} spawned in team player mode")
                            else:
                                await ctx.send("cannot execute this command in this mode")
                    flag=0
            if flag:
                await ctx.send("profile not found create one with /create_profile")
            print(multi_players)
        elif check==0:
            await ctx.send("player already spawned")
    else:
        await ctx.send("you are not playing teamplayer mode")


@client.command()
async def create_team(ctx,team_name):
    flag=1
    global teams
    global team_players
    for player in team_players:
        if int(player.get_id())==int(ctx.message.author.id):
            flag=0
            if player.get_team()=="none":
                if team_name!="none":
                    check=1
                    for item in teams:
                        if str(item.get_team_name())==str(team_name):
                            check=0
                            break
                    if check:
                        new_team=team(team_name,ctx.message.author.id)
                        player.take_team(team_name)
                        new_team.add_member(player)
                        teams.append(new_team)
                        await ctx.send(f"created a new team named {team_name} with leader {player.get_name()}")
                        break
                    else:
                        await ctx.send(f"{team_name} team name has already been taken please choose another one")
                else:
                    await ctx.send(f"please choose another team name")
                    break
            else:
                await ctx.send(f"{player.get_name()} you are already in a team")
                break
    if flag:
        await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} you have not yet spawned in team player mode")

@client.command()
async def list_team_members(ctx):
    global team_players
    global teams
    flag=0
    player=teamplayer(0,0,0,0,0,0)
    for player in team_players:
        if int(player.get_id())==int(ctx.message.author.id):
            flag=1
            break
    if flag:
        if player.get_team()=="none":
            await ctx.send(f"{player.get_name()} you are not in a team")
        else:
            for tem in teams:
                if str(tem.get_team_name())==str(player.get_team()):
                    team_members=tem.get_team_members()
                    await ctx.send(f"team name:{tem.get_team_name()}")
                    for item in team_members:
                        await ctx.send(f"name:{item.get_name()}")
                        await ctx.send(f"hp:{item.get_hp()}")
                        await ctx.send(f"damage:{item.get_damage()}")
                        await ctx.send(f"xp:{item.get_xp()}")
                    break
    else:
        await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} you have not yet spawned in team player mode")

@client.command()
async def join_team(ctx,team_name):
    global teams
    global team_players
    flag=0
    player=teamplayer(0,0,0,0,0,0)
    for player in team_players:
        if int(player.get_id())==int(ctx.message.author.id):
            flag=1
            break
    if flag:
        if player.get_team()!="none":
            await ctx.send(f"{player.get_name()} you are already in a team")
        else:
            check=1
            for tem in teams:
                if str(tem.get_team_name())==str(team_name):
                    player.take_team(team_name)
                    tem.add_member(player)
                    check=0
                    await ctx.send(f"{player.get_name()} joined {team_name}")
                    break
            if check:
                await ctx.send(f"no team named {team_name} exists")
    else:
        await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} you have not yet spawned in team player mode")

@client.command()
async def leave_team(ctx):
    global teams
    global team_players
    flag=0
    player=teamplayer(0,0,0,0,0,0)
    for player in team_players:
        if int(player.get_id())==int(ctx.message.author.id):
            flag=1
            break
    if flag:
        if player.get_team()=="none":
            await ctx.send(f"{player.get_name()} you are not in a team")
        else:
            check=1
            for tem in teams:
                if str(tem.get_team_name())==str(player.get_team()):
                    player.take_team("none")
                    tem.remove_member(player)
                    check=0
                    await ctx.send(f"{player.get_name()} left {tem.get_team_name()}")    
                    if len(tem.get_team_members())==0:
                        await ctx.send(f"team {tem.get_team_name()} removed as there were no members in it")
                        teams.remove(tem)
                        break
                    if int(tem.get_leader_id())==int(player.get_id()):
                        await ctx.send(f"leader {player.get_name()} left the team {tem.get_team_name()}")
                        members=tem.get_team_members()
                        tem.change_leader_id(members[0].get_id())
                        await ctx.send(f"{members[0].get_name()} is the new leader of team {tem.get_team_name()}")    
                    break
            if check:
                await ctx.send(f"no team named {team_name} exists")
    else:
        await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} you have not yet spawned in team player mode")

@client.command()
async def kick_member(ctx,member):
    global teams
    global team_players
    flag=1
    player=teamplayer(0,0,0,0,0,0)
    for player in team_players:
        if int(player.get_id())==int(ctx.message.author.id):
            flag=1
            break
    if flag:
        if player.get_team()=="none":
            await ctx.send(f"{player.get_name()} you are not in a team")
        else:
            for tem in teams:
                if str(tem.get_team_name())==str(player.get_team()):
                    if str(tem.get_leader_id())==str(player.get_id()):
                        member_id=''
                        j=3
                        while(member[j]!='>'):
                            member_id=(member_id+member[j])
                            j+=1
                        members=tem.get_team_members()
                        if str(player.get_id())==str(member_id):
                            await ctx.send(f"{player.get_name()} you cannot kick yourself out of the team")
                        else:
                            for item in members:
                                if str(item.get_id())==str(member_id):
                                    item.take_team("none")
                                    tem.remove_member(item)
                                    await ctx.send(f"{item.get_name()} removed from {tem.get_team_name()}")
                                    break
                    else:
                        await ctx.send(f"{player.get_name()} only leaders can kick members")
                        check=0
                        break
    else:
        await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} you have not yet spawned in team player mode")

@client.command()
async def exit_team_player(ctx):
    global team_players
    global teams
    flag=1
    for data in json_data:
        if data["id"]==ctx.message.author.id:
            if data["status"]=="team":
                data["status"]="free"
                for player in team_players:
                    if player.get_id()==ctx.message.author.id:
                        for tem in teams:
                            if str(tem.get_team_name())==str(player.get_team()):
                                player.take_team("none")
                                tem.remove_member(player)
                                check=0
                                await ctx.send(f"{player.get_name()} left {tem.get_team_name()}")    
                                if len(tem.get_team_members())==0:
                                    await ctx.send(f"team {tem.get_team_name()} removed as there were no members in it")
                                    teams.remove(tem)
                                    break
                                if int(tem.get_leader_id())==int(player.get_id()):
                                    await ctx.send(f"leader {player.get_name()} left the team {tem.get_team_name()}")
                                    members=tem.get_team_members()
                                    tem.change_leader_id(members[0].get_id())
                                    await ctx.send(f"{members[0].get_name()} is the new leader of team {tem.get_team_name()}")
                                await ctx.send(f"{player.get_name()} exits team player mode")
                                team_players.remove(player)
                                break
                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                    file.truncate(0)
                    file.seek(0)
                    file.write(json.dumps(json_data))
                    file.close()
                flag=0
                break
    if flag:
        await ctx.send("you are not in team player mode")


@client.command()
async def duel_team(ctx,member):
    num=random.randint(1,10)
    global team_players
    attacker=person(0,0,0,0,0,"xyz")
    print(attacker.get_damage())
    item=person(0,0,0,0,0,0)
    for item in team_players:
        if int(item.get_id())==int(ctx.message.author.id):
            attacker=teamplayer(item.get_maxhp(),item.get_xp(),item.get_name(),item.get_damage(),item.get_id(),item.get_status())
            attacker.take_team(item.get_team())
            print("attacker found")
            break
    if str(item.get_status())=="team":
        if attacker.get_damage()==0:
            await ctx.send("you have not spawned yet")
        elif attacker.get_damage():
            flag=1
            member_id=''
            j=3
            while(member[j]!='>'):
                member_id=(member_id+member[j])
                j+=1
            print("here")
            print(team_players)
            print(member_id)
            print(ctx.message.author.id)
            if int(member_id)==int(ctx.message.author.id):
                await ctx.send("you cannot attack yourself ")
            else:
                for player in team_players:
                    print("inside for loop")
                    print(player.get_id())
                    print(member_id)
                    print("team",player.get_team())
                    if str(player.get_id())==str(member_id) and str(player.get_id())!=str(attacker.get_id()):
                        if str(player.get_team())==str(attacker.get_team()):
                            await ctx.send(f"{attacker.get_name()} you cannot attack your team member{player.get_name()}")
                            flag=0
                        else:
                            flag=0
                            if player.get_team()=="none":
                                await ctx.send(f"{player.get_name()} is not a part of any team you cannot attack him")
                            elif attacker.get_team()=="none":
                                await ctx.send(f"{attacker.get_name()} you are not a part of any team you cannot attack others")
                            else:
                                dmg=attacker.generate_damage()
                                player.take_damage(dmg)
                                await ctx.send(f"{attacker.get_name()} attacked {player.get_name()} for {dmg} hp")
                                print("hp:",player.get_hp())
                                if player.get_hp()<=0:
                                    for tem in teams:
                                        if str(tem.get_team_name())==str(player.get_team()):
                                            player.take_team("none")
                                            tem.remove_member(player)
                                            check=0
                                            await ctx.send(f"{player.get_name()} left {tem.get_team_name()} as he died")    
                                            if len(tem.get_team_members())==0:
                                                await ctx.send(f"team {tem.get_team_name()} removed as there were no members in it")
                                                teams.remove(tem)
                                                break
                                            if int(tem.get_leader_id())==int(player.get_id()):
                                                await ctx.send(f"leader {player.get_name()} left the team {tem.get_team_name()} as he died")
                                                members=tem.get_team_members()
                                                tem.change_leader_id(members[0].get_id())
                                                await ctx.send(f"{members[0].get_name()} is the new leader of team {tem.get_team_name()}")
                                                await ctx.send(f"{player.get_name()} exits team player mode")
                                            break
                                    for item in json_data:
                                        if item["name"]==ctx.message.author.name+'#'+ctx.message.author.discriminator:
                                            item["xp"]+=10
                                            await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} have been awarded 10 xp")
                                        if (item["name"])==str(player.get_name()):
                                            item["status"]="free"
                                    with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                        file.truncate(0)
                                        file.seek(0)
                                        file.write(json.dumps(json_data))
                                        file.close()
                                    team_players.remove(player)
                                break
                if flag:
                    await ctx.send("no such player found or player dead")                    
    else:
        await ctx.send("you are currently not playing team player mode cannot execute this command")

@client.command()
async def rage_team(ctx,member):
    num=random.randint(1,10)
    global team_players
    attacker=person(0,0,0,0,0,"xyz")
    print(attacker.get_damage())
    item=person(0,0,0,0,0,0)
    for item in team_players:
        if int(item.get_id())==int(ctx.message.author.id):
            attacker=teamplayer(item.get_maxhp(),item.get_xp(),item.get_name(),item.get_damage(),item.get_id(),item.get_status())
            attacker.take_team(item.get_team())
            print("attacker found")
            break
    if str(item.get_status())=="team":
        if attacker.get_damage()==0:
            await ctx.send("you have not spawned yet")
        elif attacker.get_damage():
            flag=1
            member_id=''
            j=3
            while(member[j]!='>'):
                member_id=(member_id+member[j])
                j+=1
            print("here")
            print(team_players)
            print(member_id)
            print(ctx.message.author.id)
            if int(member_id)==int(ctx.message.author.id):
                await ctx.send("you cannot attack yourself ")
            else:
                for player in team_players:
                    print("inside for loop")
                    print(player.get_id())
                    print(member_id)
                    print("team",player.get_team())
                    if str(player.get_id())==str(member_id) and str(player.get_id())!=str(attacker.get_id()):
                        if str(player.get_team())==str(attacker.get_team()):
                            await ctx.send(f"{attacker.get_name()} you cannot attack your team member{player.get_name()}")
                            flag=0
                        else:
                            flag=0
                            if player.get_team()=="none":
                                await ctx.send(f"{player.get_name()} is not a part of any team you cannot attack him")
                            elif attacker.get_team()=="none":
                                await ctx.send(f"{attacker.get_name()} you are not a part of any team you cannot attack others")
                            else:
                                if attacker.get_xp()>=5:
                                    print("xp:",attacker.get_xp())
                                    item.reduce_xp(5)
                                    print("changed xp in class")
                                    print("xp:",attacker.get_xp())
                                    for data in json_data:
                                        if data["id"]==attacker.get_id():
                                            data["xp"]-=5
                                            print("5 xp deducted")
                                    with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                        file.truncate(0)
                                        file.seek(0)
                                        file.write(json.dumps(json_data))
                                        file.close()
                                    await ctx.send(f"5 xp deducted from {attacker.get_name()}")
                                    dmg=attacker.generate_damage()
                                    dmg+=10
                                    player.take_damage(dmg)
                                    await ctx.send(f"{attacker.get_name()} attacked extensively {player.get_name()} for {dmg} hp")
                                    print("hp:",player.get_hp())
                                else:
                                    await ctx.send("insufficient xp")
                                if player.get_hp()<=0:
                                    for tem in teams:
                                        if str(tem.get_team_name())==str(player.get_team()):
                                            player.take_team("none")
                                            tem.remove_member(player)
                                            check=0
                                            await ctx.send(f"{player.get_name()} left {tem.get_team_name()} as he died")    
                                            if len(tem.get_team_members())==0:
                                                await ctx.send(f"team {tem.get_team_name()} removed as there were no members in it")
                                                teams.remove(tem)
                                                break
                                            if int(tem.get_leader_id())==int(player.get_id()):
                                                await ctx.send(f"leader {player.get_name()} left the team {tem.get_team_name()} as he died")
                                                members=tem.get_team_members()
                                                tem.change_leader_id(members[0].get_id())
                                                await ctx.send(f"{members[0].get_name()} is the new leader of team {tem.get_team_name()}")
                                                await ctx.send(f"{player.get_name()} exits team player mode")
                                            break
                                    for item in json_data:
                                        if item["name"]==ctx.message.author.name+'#'+ctx.message.author.discriminator:
                                            item["xp"]+=10
                                            await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} have been awarded 10 xp")
                                        if (item["name"])==str(player.get_name()):
                                            item["status"]="free"
                                    with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                        file.truncate(0)
                                        file.seek(0)
                                        file.write(json.dumps(json_data))
                                        file.close()
                                    team_players.remove(player)
                                break
                if flag:
                    await ctx.send("no such player found or player dead")                    
    else:
        await ctx.send("you are currently not playing team player mode cannot execute this command")

@client.command()
async def heal_team(ctx,member):
    global team_players
    attacker=person(0,0,0,0,0,"xyz")
    print(attacker.get_damage())
    item=person(0,0,0,0,0,0)
    for item in team_players:
        if int(item.get_id())==int(ctx.message.author.id):
            attacker=teamplayer(item.get_maxhp(),item.get_xp(),item.get_name(),item.get_damage(),item.get_id(),item.get_status())
            attacker.take_team(item.get_team())
            print("attacker found")
            break
    if str(item.get_status())=="team":
        if attacker.get_damage()==0:
            await ctx.send("you have not spawned yet")
        elif attacker.get_damage():
            flag=1
            member_id=''
            j=3
            while(member[j]!='>'):
                member_id=(member_id+member[j])
                j+=1
            print("here")
            print(team_players)
            print(member_id)
            print(ctx.message.author.id)
            for player in team_players:
                print("inside for loop")
                print(player.get_id())
                print(member_id)
                print("team",player.get_team())
                if str(player.get_id())==str(member_id):
                    flag=0
                    if player.get_team()=="none":
                        await ctx.send(f"{player.get_name()} is not a part of any team you cannot heal him")
                    elif attacker.get_team()=="none":
                        await ctx.send(f"{attacker.get_name()} you are not a part of any team you cannot heal others")
                    else:
                        if attacker.get_xp()>=8:
                            print("xp:",attacker.get_xp())
                            item.reduce_xp(8)
                            print("changed xp in class")
                            print("xp:",attacker.get_xp())
                            for data in json_data:
                                if data["id"]==attacker.get_id():
                                    data["xp"]-=8
                                    print("8 xp deducted")
                            with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                file.truncate(0)
                                file.seek(0)
                                file.write(json.dumps(json_data))
                                file.close()
                            await ctx.send(f"8 xp deducted from {attacker.get_name()}")
                            player.take_damage(-player.get_maxhp())
                            await ctx.send(f"{attacker.get_name()} healed {player.get_name()}")
                            print("hp:",player.get_hp())
                        else:
                            await ctx.send("insufficient xp")
                        if player.get_hp()<=0:
                            for tem in teams:
                                if str(tem.get_team_name())==str(player.get_team()):
                                    player.take_team("none")
                                    tem.remove_member(player)
                                    check=0
                                    await ctx.send(f"{player.get_name()} left {tem.get_team_name()} as he died")    
                                    if len(tem.get_team_members())==0:
                                        await ctx.send(f"team {tem.get_team_name()} removed as there were no members in it")
                                        teams.remove(tem)
                                        break
                                    if int(tem.get_leader_id())==int(player.get_id()):
                                        await ctx.send(f"leader {player.get_name()} left the team {tem.get_team_name()} as he died")
                                        members=tem.get_team_members()
                                        tem.change_leader_id(members[0].get_id())
                                        await ctx.send(f"{members[0].get_name()} is the new leader of team {tem.get_team_name()}")
                                        await ctx.send(f"{player.get_name()} exits team player mode")
                                    break
                            for item in json_data:
                                if item["name"]==ctx.message.author.name+'#'+ctx.message.author.discriminator:
                                    item["xp"]+=10
                                    await ctx.send(f"{ctx.message.author.name+'#'+ctx.message.author.discriminator} have been awarded 10 xp")
                                if (item["name"])==str(player.get_name()):
                                    item["status"]="free"
                            with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                file.truncate(0)
                                file.seek(0)
                                file.write(json.dumps(json_data))
                                file.close()
                            team_players.remove(player)
                        break
            if flag:
                await ctx.send("no such player found or player dead")                    
    else:
        await ctx.send("you are currently not playing team player mode cannot execute this command")



client.run('token')
