import discord
import asyncio
import time
import random
import views
import functions
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

VERSION = "v. 0.2a"


# ========== ADMINISTRATIVE/FUNCTIONAL COMMANDS ==========

# puts an embed in the text chat to kick a member of the voice chat
@tree.command(name="vote_kick", description="vote to kick from call")
async def vote_kick(interaction, target: discord.Member):
    """
    initiates a vote kick on the targeted user
    :param target: the targeted user, type: discord.Member
    :return:
    """
    event_name = "vote_kick"  # used for console_output()
    event_result = ""  # used for console_output()
    current_channel = interaction.user.voice  # shortcut to voice channel of vote starter
    current_voice_members = []  # stores a snapshot of the voice channel members at the time of the vote
    start_time = 0  # starting time of the vote

    if current_channel is None:
        await interaction.response.send_message("You're not in a voice channel :(", ephemeral=True)
        event_result = "user not in voice channel"

    else:
        # stores current members of voice channel
        for member in current_channel.channel.members:
            current_voice_members.append(member.id)
        view = views.KickButtons(current_voice_members)

        # checks if the targeted user is in the voice call
        if target.id not in current_voice_members:
            await interaction.response.send_message("That person isn't in your call :3", ephemeral=True)
            event_result = "target not in the same voice channel"

        else:
            # sends vote message
            await interaction.response.send_message("Vote To Kick: " + target.display_name, view=view)
            start_time = time.time()

            # keeps the vote open unless the majority has voted yes, half has voted no, or 15 seconds have passed
            # this is because ties result in no kick, which means only half need to vote no
            while view.yesVotes <= (len(view.eligibleIDs) / 2) and view.noVotes < (len(view.eligibleIDs) / 2) \
                    and time.time() - start_time < 15:
                await asyncio.sleep(1)

            # vote result logic
            if view.yesVotes > view.noVotes:
                event_result = "vote passed"
                await target.move_to(None)
                await interaction.edit_original_response(content="Ok, kicked " + target.display_name + \
                                                                 "\n Yes: " + str(view.yesVotes) + \
                                                                 " | No: " + str(view.noVotes), view=None)
            else:
                event_result = "vote failed"
                await interaction.edit_original_response(content="Vote kick on " + target.display_name + " failed" \
                                                                 "\n Yes: " + str(view.yesVotes) + \
                                                                 " | No: " + str(view.noVotes), view=None)

    functions.console_output(event_name, interaction.user.id, target.id, event_result)


# ========== FUN COMMANDS ==========

@tree.command(name="uwuify", description="uwuify a sentance")
async def uwuify(interaction, message: str, hidden: bool = True):
    # all the logic is handled by functions.uwuify
    event_name = "uwuify"
    await interaction.response.send_message(content=functions.uwuify(message), ephemeral=hidden)
    functions.console_output(event_name, interaction.user.id)


# just passes the message through to chat useful for testing the bot and making jokes
@tree.command(name="say", description="I'll say something in chat for you (don't abuse this)")
async def say(interaction, message: str):
    event_name = "say"
    await interaction.response.send_message(content=message)
    functions.console_output(event_name, interaction.user.id, outcome=message)


# flips a coin
@tree.command(name="coinflip", description="flips a coin")
async def coinflip(interaction):
    # detemine outcome
    event_name = "coinflip"
    coin = "Heads" if random.randint(1, 2) == 1 else "Tails"
    embed = discord.Embed(title=coin)
    # set proper thumbnail for outcome
    if coin == "Heads":
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/2006_Quarter_Proof.png/780px-2006_Quarter_Proof.png")
    else:
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/5/5a/98_quarter_reverse.png")
    await interaction.response.send_message(embed=embed)
    functions.console_output(event_name, interaction.user.id, outcome=coin)


# returns a random number between user specified min and max
@tree.command(name="random_number", description="provides random number between min and max.")
async def random_number(interaction, minimum: int, maximum: int, hidden: bool = False):
    event_name = "random_number"
    return_message = ""
    console_message = ""
    if minimum >= maximum:
        return_message = "The maximum has to be bigger than the minimum dummy :3"
        console_message = "Invalid Parameters"
        hidden = True  # overrides user given value, hides message in case of error message
    else:
        number = random.randint(minimum, maximum)
        console_message = number
        return_message = number

    embed = discord.Embed(title=return_message)
    await interaction.response.send_message(embed=embed, ephemeral=hidden)
    functions.console_output(event_name, interaction.user.id, outcome=console_message)


# plays rock paper scissors with the user
@tree.command(name="rock_paper_scissors", description="Play rock paper scissors.")
async def rock_paper_scissors(interaction, hidden: bool = False):
    view = views.RPSButtons()  # buttons
    start_time = time.time()  # start time, used for a 30-second timer
    bot_choice = ""  # stores the bots choice
    result = ""
    win = "You win!"
    lose = "You lost..."

    await interaction.response.send_message(content="Make your choice:", view=view, ephemeral=hidden)
    while view.player_choice is None and time.time() - 30 < start_time:
        await asyncio.sleep(1)
    if view.player_choice is None:
        interaction.edit_original_response(content="I'm going to sleep.", view=None)

    else:
        bot_choice = view.choices[random.randint(0, 2)]
        if bot_choice == view.player_choice:
            result = "It's a tie!"
        elif view.win_dict[view.player_choice] == bot_choice:
            result = win
        elif view.win_dict[bot_choice] == view.player_choice:
            result = lose
        await interaction.edit_original_response(content=result + "\nYOU | UwU \n " +
                                                 view.icons[view.player_choice] +
                                                 "     " + view.icons[bot_choice], view=None)


# ========== INFORMATIONAL COMMANDS ==========

@tree.command(name="info", description="gives information about the bot")
async def info(interaction):
    """
    sends information on the bot to the invoker
    :return: none
    """
    event_name = "info"
    embed = discord.Embed(title="UwU Bot", description=VERSION)
    embed.add_field(name="Lead Dev:", value="⠀⠀SpySandwiches")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    functions.console_output(event_name, interaction.user.id)


@tree.command(name="patch", description="shows the latest patch notes")
async def patch(interaction, hidden: bool = True):
    """
    Shows the latest patch from readme.md
    :return: none
    """
    event_name = "patch"
    embed = discord.Embed(title="UwU Bot", description="UwU bot (internally NUwU) is my personal discord bot")
    with open("readme.md") as infile:
        for line in infile:
            # skips title and description, as they have to be set on initialization of the embed object
            if line == "# UwU bot\n" or line == "UwU bot (internally NUwU) is my personal discord bot\n":
                pass
            # adds version label to the name of the field instead of the value, makes it slightly larger
            elif line[0:4] == "# v.":
                embed.add_field(name=line[1:-1], value="", inline=False)
            # same as above for change categories, but ignores more of the #'s
            elif line[0] == '#':
                embed.add_field(name=line[3:-1], value="", inline=False)
            else:
                embed.add_field(name="", value=line[1:-1], inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=hidden)
    functions.console_output(event_name, interaction.user.id)


# ========== DRIVER ==========

# on ready
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for femboys OwO"))

client.run("secret")


# todo
# tic tac toe
# add unfair mode to RPS (can't win)
# add rematch to RPS
# make fancy embed for RPS
# rewrite vote_kick output to be a fancy embed
# find cool shit to add
