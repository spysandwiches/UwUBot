import os

import discord
import asyncio
import time
import random

import dataStructures
import views
import functions
import json
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

VERSION = "v. 0.2.2a"

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


# probably getting rewritten
@tree.command(name="play_song", description="Plays a song from youtube. Don't tell discord ;)")
async def play_song(interaction, link: str, volume: float = 0.6):
    connected = False  # tests for bot already being connected
    temp_name = ""  # holds name of song for dataStructures.QueuedSong
    temp_path = ""  # holds path for song
    guild_id = interaction.guild_id
    current_directory = os.getcwd().replace("\\", "/")
    if "www.youtube.com" not in link:
        await interaction.response.send_message("Bad Link.")
    else:
        voice_channel = interaction.user.voice.channel
        if volume > 1.5:
            volume = 1.5
        elif volume < .01:
            volume = .01

        # checking if bot is already in this server's vc
        for vc in client.voice_clients:
            if voice_channel == vc.channel:
                connected = True  # prevents bot from trying to rejoin vc

        if connected:
            await interaction.response.send_message("Adding...")

        else:
            await interaction.response.send_message("Fetching song, this could take a minute. (" +
                                                    await functions.get_song_name(link) + ")")

        # add song to queue
        if interaction.guild_id not in client.music_queue:  # initializing new server
            client.music_queue[guild_id] = []
        temp_path, temp_name = await functions.get_youtube_vid(current_directory, link)  # getting song
        temp_path = temp_path.replace("\\", "/")  # formatting file path
        # storing QueuedSong object in client.music_queue
        client.music_queue[guild_id].append(dataStructures.QueuedSong(temp_path, temp_name))

        if connected:
            await interaction.edit_original_response(content=("Added: " + await functions.get_song_name(link) +
                                                              " to the queue"))

        # not connected, acts as loop
        if not connected:
            voice_client = await voice_channel.connect()
            while len(client.music_queue[guild_id]) > 0:  # while music is queued
                current_path = client.music_queue[guild_id][0].file_path
                current_name = client.music_queue[guild_id][0].real_name
                player = discord.FFmpegPCMAudio(current_path, executable=(current_directory + "/dependencies/ffmpeg"),
                                                options='-filter:a "volume=' + str(volume) + '"')
                # play song
                voice_client.play(player)
                while voice_client.is_playing():
                    await asyncio.sleep(5)
                # delete played song
                os.remove(client.music_queue[guild_id][0].file_path)
                del client.music_queue[guild_id][0]
            await voice_client.disconnect()


# shows music_queue for current server
@tree.command(name="show_queue", description="shows current music queue")
async def show_queue(interaction):
    message = ""
    if interaction.guild_id not in  client.music_queue:
        message = "no songs queued..."
    else:
        for song in client.music_queue[interaction.guild_id]:
            message += song.real_name + "\n"
        if message is None:
            message = "no songs queued..."

    await interaction.response.send_message(message)


# ========== FUN COMMANDS ==========

@tree.command(name="uwuify", description="uwuify a sentance")
async def uwuify(interaction, message: str, hidden: bool = True):
    # all the logic is handled by functions.uwuify
    event_name = "uwuify"
    await interaction.response.send_message(content=functions.uwuify(message), ephemeral=hidden)
    functions.console_output(event_name, interaction.user.id)


@tree.command(name="leet_speak", description="1337 sp34k a sentance")
async def leet_speak(interaction, message: str, hidden: bool = True):
    # all the logic is handled by functions.uwuify
    event_name = "leetspeak"
    await interaction.response.send_message(content=functions.leet_speak(message), ephemeral=hidden)
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
    event_name = "RPS"
    view = views.RPSButtons()  # buttons
    rematch_view = views.RPSRematch()  # rematch button
    start_time = time.time()  # start time, used for a 30-second timer
    finished = False  # used to stop loop, determined by rematch button
    result = ""  # stores win/loss for output message

    # send original message
    await interaction.response.send_message(content="Make your choice:", view=view, ephemeral=hidden)

    # main loop
    while not finished:
        # resetting variables for new round upon rematch
        if rematch_view.clicked:
            await interaction.edit_original_response(content="Make your choice:", view=view)
            view.bot_choice = None
            view.player_choice = None
            rematch_view.clicked = False
            start_time = time.time()
            result = ""

        # starts timer, waits for plaer choice
        while view.player_choice is None and time.time() - 30 < start_time:
            await asyncio.sleep(1)
        # catches time out
        if view.player_choice is None:
            await interaction.edit_original_response(content="I'm going to sleep.", view=None)
            finished = True
            result = "Timed out"
        else:
            view.bot_choice = view.choices[random.randint(0, 2)]  # picks bot choice
            # win logic
            if view.bot_choice == view.player_choice:
                result = "It's a tie!"
            elif view.win_dict[view.player_choice] == view.bot_choice:
                result = "You win!"
            elif view.win_dict[view.bot_choice] == view.player_choice:
                result = "You lost..."
            # output
            await interaction.edit_original_response(content=result + "\nYOU | UwU \n" +
                                                     view.icons[view.player_choice] +
                                                     "     " + view.icons[view.bot_choice], view=rematch_view)
            # timer for rematch button
            start_time = time.time()
            while not rematch_view.clicked and time.time() - 60 < start_time:
                await asyncio.sleep(1)
            # if rematch button isn't clicked
            if not rematch_view.clicked:
                finished = True
                # resends response without rematch button
                await interaction.edit_original_response(content=result + "\nYOU | UwU \n" +
                                                         view.icons[view.player_choice] +
                                                         "     " + view.icons[view.bot_choice], view=None)
        # loop restarts here, rematch button being pressed causes another pass through,
        # no press will result in the loop ending
    functions.console_output(event_name, interaction.user.id, outcome=result)


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
                embed.add_field(name="==" + line[3:-1] + "==", value="", inline=False)
            else:
                embed.add_field(name="", value=line[1:-1], inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=hidden)
    functions.console_output(event_name, interaction.user.id)


# ========== DRIVER ==========

# on ready
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you sleep."))
    client.music_queue = {} # stores guild_ids which hold lists of dataStructures.QueuedSong objects
    functions.startup_display()


# on message, used for warning user's to turn @'s off on replies
@client.event
async def on_message(message):
    message_author = str(message.author.id)
    raw_file = open('reply_mentions_storage.json', 'r')
    infile = json.load(raw_file)

    # initialize unrecognized user
    if message_author not in infile['ids'].keys():
        infile['ids'][message_author] = {"timestamps": [],
                                         "last_warning": 0}

    # checks if message is a reply
    if message.reference is not None:
        original_channel = await client.fetch_channel(message.reference.channel_id)
        original_message = await original_channel.fetch_message(message.reference.message_id)

        # checks if reply mentions the original commentor
        for mention in message.mentions:
            if mention == original_message.author:

                # deletes timestamps older than 48 hours
                current_time = time.time()
                for timestamp in infile['ids'][message_author]["timestamps"]:
                    if current_time - timestamp > 172800:
                        infile['ids'][message_author]["timestamps"].pop(timestamp)

                # triggers warning if more than 2 @'s in the past 24 hours
                if len(infile['ids'][message_author]["timestamps"]) >= 2:
                    if time.time() - infile['ids'][message_author]["last_warning"] > 86400:
                        send_message = "<@" + message_author + \
                                       "> Hey, you've been replying to people without turning " \
                                       "the @ off. This is incredibly fucking annoying.\n" \
                                       "turn it off."
                        await original_channel.send(content=send_message)
                        infile['ids'][message_author]["last_warning"] = time.time()
                        functions.console_output("Warned user for reply @'s", message_author)
                    else:
                        functions.console_output("Warned user for reply @'s", message_author, outcome="on cooldown")
                    infile['ids'][message_author]["timestamps"].clear()

                # adds a strike
                else:
                    infile['ids'][message_author]["timestamps"].append(time.time())
                    functions.console_output("Added @ strike", message_author)

    with open('reply_mentions_storage.json', 'w') as outfile:
        json.dump(infile, outfile, indent=4, sort_keys=True)


client.run("token")



# todo
# make @ warning configurable
# make @ warning based on server
# /play_song sucks
# switch off pytube for /play_song (throws giant errors but still works, seems to be a bug)
# bad apple status
# better documentation
# tic tac toe
# add support for 2 player games (rps, tic-tac-toe, etc.)
# add support for more than 1 number from /random_number
# make fancy embed for RPS
# rewrite vote_kick output to be a fancy embed
# add chess (large project)
# minesweeper (large project)
# find cool shit to add
