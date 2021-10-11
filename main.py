import uwuifier
import json
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='>uwu ')

bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='">uwu help" for help'))


@bot.event
async def on_guild_join(guild):
    print("joined", guild.id)
    with open('data.json', 'r') as infile:
        data = json.load(infile)
    data['servers'][str(guild.id)] = {}
    data['servers'][str(guild.id)]['targetedUsers'] = []
    data['servers'][str(guild.id)]['targetedChannels'] = []
    data['servers'][str(guild.id)]['disqualifyingCharacters'] = ['<']
    data['servers'][str(guild.id)]['admins'] = ['209785453505675275']
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)


# useless really
def check_access(sender):
    newsender = str(sender)
    with open('data.json', 'r') as infile:
        data = json.load(infile)
    if newsender in data['targetedUsers']:
        if newsender in data['admins']:
            return True
        else:
            return False

    return True


def check_admin(sender, server):
    newsender = str(sender)
    with open('data.json', 'r') as infile:
        data = json.load(infile)
    if newsender in data['servers'][str(server)]['admins']:
        return True
    else:
        return False


@bot.command()
async def help(ctx):
    embedmsg = "> help \n I really hope that's not why you came here.\n\n" \
               "> addadmin <user> \n accepts @ or user ID, forces commands to work. Requires admin\n\n" \
               "> removeadmin \n @Spysandwiches for use.\n\n" \
               "> addfemboy <user> \n accepts @ or user ID, adds user to list. Requires admin\n\n" \
               "> removefemboy <user> \n same thing but it removes. Requires admin\n\n" \
               "> addchannel <channel> \n adds channel to bot whitelist, defaults to current channel. Requires admin\n\n" \
               "> removechannel <channel> \n same thing but it removes. Requires admin\n\n" \
               "> listfemboys \n see who the bottoms are\n\n" \
               "> listchannels \n see where i'm allowed to talk\n\n"

    embed = discord.Embed(title="Help me pwease!", description=embedmsg)
    await ctx.send(embed=embed)


# adds user to targets list
@bot.command()
async def addfemboy(ctx, arg):
    if not check_admin(ctx.message.author.id, ctx.message.author.guild.id):
        await ctx.send("Aww you think I listen to you? Adorable")
        return()
    if arg[0] == "<":
        arg = arg[3:-1]
    try:
        await bot.fetch_user(arg)
    except:
        await ctx.send("That's not a real person!")
        return()

    with open('data.json', 'r+') as infile:
        data = json.load(infile)
    for user in data['servers'][str(ctx.message.author.guild.id)]['targetedUsers']:
        if arg == user:
            print("Femboy already in database. skipping.")
            await ctx.send("I already know they're a femboy UwU")
            return()
    data['servers'][str(ctx.message.author.guild.id)]['targetedUsers'].append(arg)
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
    await ctx.send("Added to the list, have fun OwO")
    print("Femboy added!", arg)
    return()


@bot.command()
async def removefemboy(ctx, arg):
    if not check_admin(ctx.message.author.id, ctx.message.author.guild.id):
        await ctx.send("Aww you think I listen to you? Adorable")
        return()
    if arg[0] == "<":
        arg = arg[3:-1]

    try:
        await bot.fetch_user(arg)
    except:
        await ctx.send("That's not a real person!")
        return()


    with open('data.json', 'r+') as infile:
        data = json.load(infile)
    try:
        data['servers'][str(ctx.message.author.guild.id)]['targetedUsers'].remove(arg)
    except(ValueError):
        await ctx.send("I don't know that person. Perhaps you should introduce us first?")
        return()
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
    await ctx.send("Removed from the list. Bai bai :3")
    print("Femboy removed!", arg)
    return()


@bot.command()
async def addadmin(ctx, arg=None):
    with open('data.json', 'r') as infile:
        data = json.load(infile)
    if str(ctx.message.author.id) not in data['admins']:
        await ctx.send("You have to be an admin to make an admin. Duh")
    if arg is not None and arg[0] == "<":
        arg = arg[3:-1]

    try:
        await bot.fetch_user(arg)
    except:
        await ctx.send("That's not a real person!")
        return()


    with open('data.json', 'r') as infile:
        data = json.load(infile)
        for admin in data['servers'][str(ctx.message.author.guild.id)]['admins']:
            if admin == arg:
                await ctx.send("I'm already accepting commands from them!")
                return()
        data['servers'][str(ctx.message.author.guild.id)]['admins'].append(arg)
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
        await ctx.send("Alright, I'll listen to them from now on!")


@bot.command()
async def addchannel(ctx, arg=None):
    if not check_admin(ctx.message.author.id, ctx.message.author.guild.id):
        await ctx.send("Aww you think I listen to you? Adorable")
        return()
    if arg is not None and arg[0] == "<":
        arg = arg[2:-1]
    elif arg is not None:
        pass
        # stops else from triggering if raw channel id is input
    else:
        arg = str(ctx.message.channel.id)

    try:
        await bot.fetch_channel(arg)
    except:
        await ctx.send("That's not a real channel!")
        return ()

    with open('data.json', 'r+') as infile:
        data = json.load(infile)
    for channel in data['servers'][str(ctx.message.author.guild.id)]['targetedChannels']:
        if arg == channel:
            print("Channel already in database. skipping.")
            await ctx.send("I'm already allowed in that channel hehe")
            return()
    data['servers'][str(ctx.message.author.guild.id)]['targetedChannels'].append(arg)
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
    await ctx.send("Added to the list, have fun OwO")
    print("Channel added!", arg)
    return()


@bot.command()
async def removechannel(ctx, arg=None):
    if not check_admin(ctx.message.author.id, ctx.message.author.guild.id):
        await ctx.send("Aww you think I listen to you? Adorable")
        return()
    if arg is not None and arg[0] == "<":
        arg = arg[2:-1]
    elif arg is not None:
        pass
        # stops else from triggering if raw channel id is input
    else:
        arg = str(ctx.message.channel.id)

    try:
        await bot.fetch_channel(arg)
    except:
        await ctx.send("That's not a real channel!")
        return()

    with open('data.json', 'r+') as infile:
        data = json.load(infile)
    try:
        data['servers'][str(ctx.message.author.guild.id)]['targetedChannels'].remove(arg)
    except ValueError:
        await ctx.send("I'm not even allowed in there!")
        return()
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
    await ctx.send("Ok, I'll leave that channel alone UnU")
    print("Channel removed", arg)
    return()


@bot.command()
async def addavoidchar(ctx, arg):
    if not check_admin(ctx.message.author.id, ctx.message.author.guild.id):
        await ctx.send("Aww you think I listen to you? Adorable")
        return()
    if len(arg) > 1:
        await ctx.send("It has to be a single character.")
        return()
    with open('data.json', 'r+') as infile:
        data = json.load(infile)
        for char in data['servers'][str(ctx.message.author.guild.id)]['disqualifyingCharacters']:
            if char == arg:
                await ctx.send("I already avoid that character")
                return()
        data['servers'][str(ctx.message.author.guild.id)]['disqualifyingCharacters'].append(arg)
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
        await ctx.send("Alright, I'll avoid that from now on!")
        return()


@bot.command()
async def removeavoidchar(ctx, arg):
    if not check_admin(ctx.message.author.id, ctx.message.author.guild.id):
        await ctx.send("Aww you think I listen to you? Adorable")
        return()
    if len(arg) > 1:
        await ctx.send("It has to be a single character.")
        return()
    with open('data.json', 'r+') as infile:
        data = json.load(infile)
        try:
            data['servers'][str(ctx.message.author.guild.id)]['disqualifyingCharacters'].remove(arg)
        except(ValueError):
            await ctx.send("I don't avoid that character!")
            return()
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
        await ctx.send("Alright, I'll stop avoiding that!")
        return()


@bot.command()
async def listfemboys(ctx):
    embedmsg = ""
    with open('data.json', 'r+') as infile:
        data = json.load(infile)
        for user in data['servers'][str(ctx.message.author.guild.id)]['targetedUsers']:
            newuser = await bot.fetch_user(user)
            embedmsg += newuser.name + "#" + newuser.discriminator + "\n"

    embed = discord.Embed(title="The subs", description=embedmsg)
    await ctx.send(embed=embed)


@bot.command()
async def listchannels(ctx):
    embedmsg = ""
    with open('data.json', 'r+') as infile:
        data = json.load(infile)
        for channel in data['servers'][str(ctx.message.author.guild.id)]['targetedChannels']:
            newchannel = await bot.fetch_channel(channel)
            embedmsg += newchannel.name + "\n"

    embed = discord.Embed(title="Channels", description=embedmsg)
    await ctx.send(embed=embed)


# checks targeted user and channel, then executes UwU shit
@bot.listen()
async def on_message(message):
    print(message)
    if message.author.name == "UwU Bot":
        print("self message.")
        return()

    with open('data.json', 'r+') as f:
        print("checking disq.char...")
        data = json.load(f)
        for char in data['servers'][str(message.author.guild.id)]['disqualifyingCharacters']:
            if char == message.content[0]:
                print("message disqualified,", char, "detected")
                return()
        print("checking channels...")
        for item in data['servers'][str(message.author.guild.id)]['targetedChannels']:
            if item == str(message.channel.id):
                print("checking user...")
                for user in data['servers'][str(message.author.guild.id)]['targetedUsers']:
                    if user == str(message.author.id):
                        # FEMBOY DETECTED
                        print("femboy found, user:", message.author.name, "said:", message.content + ". UwUing.")
                        sendMsg = message.author.name + " says: " + uwuifier.makeuwu(message.content)
                        await message.channel.send(sendMsg)
                        await message.delete()
    return()
bot.run("no")



# TODO
# rewrite for loops as 'in/not in'
# find other stuff

