import discord
from discord.ext import commands
import random
from characters.classes import person
from characters.classes import _member
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
                    await ctx.send(f"you attacked attack for {dmg} hp")
                    dmg=enemy.generate_damage()
                    player.take_damage(dmg)
                    await ctx.send(f"goblin attacked you for {dmg} hp")
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
                    await ctx.send(f"goblin attacked you for {dmg} hp")
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
                for player in single_opponents:
                    if player.get_id()==ctx.message.author.id:
                        single_opponents.remove(player)
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
    for player in multi_players:
        print("listing")
        await ctx.send(f"name:{player.get_name()}")
        await ctx.send(f"hp:{player.get_hp()}")
        await ctx.send(f"xp:{player.get_xp()}")

@client.command(aliases=['duel'])
async def attack_1(ctx,member):
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
                        dmg=attacker.generate_damage()
                        print(dmg)
                        print(attacker.get_damage())
                        player.take_damage(dmg)
                        flag=0
                        await ctx.send("attacked")
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
                            attacker.reduce_xp(5)
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
                            await ctx.send("attacked")
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
                        healer.reduce_xp(8)
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
                        await ctx.send("healed")
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
    var=0
    print(json_data)
    for data in json_data:
        if str(data["id"])==str(ctx.message.author.id):
            if data["status"]=="free":
                var=1
                break
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
                            data["status"]="multi"
                            with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                                file.truncate(0)
                                file.seek(0)
                                file.write(json.dumps(json_data))
                                file.close()
                    flag=0
                    multi_players.append(new_person)
                    await ctx.send(f"{item.get_member_name()} spawned")
            if flag:
                await ctx.send("profile not found create one with /create_profile")
            print(multi_players)
        elif check==0:
            await ctx.send("player already spawned")
    else:
        await ctx.send("you are not playing multiplayer mode")


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


@client.command()
async def exit_multi_player(ctx):
    flag=1
    for data in json_data:
        if data["id"]==ctx.message.author.id:
            if data["status"]=="multi":
                data["status"]="free"
                for player in single_players:
                    if player.get_id()==ctx.message.author.id:
                        single_players.remove(player)
                for player in single_opponents:
                    if player.get_id()==ctx.message.author.id:
                        single_opponents.remove(player)
                with open(r"C:\Users\Kunj R. Patel\Desktop\python\BOT\data.json","r+") as file:
                    file.truncate(0)
                    file.seek(0)
                    file.write(json.dumps(json_data))
                    file.close()
                flag=0
                break
    if flag:
        await ctx.send("you are not in multi player mode")

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

client.run('')