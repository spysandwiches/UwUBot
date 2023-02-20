import discord
import asyncio
import time
import views
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

VERSION = "v. 0.1.1a"


def console_output(event, creator, target=None, outcome=None):
    """
    outputs to console for debugging purposes
    :param event: the event, pass an arbitrary string (i.e. "vote_kick" for vote_kick)
    :param creator: the user id of the user that invoked the command
    :param target: the user id of the target, if one exists
    :param outcome: arbitrary string of outcome, (i.e. "vote passed" or "vote failed" for vote_kick)
    :return: nothing
    """
    print("event:", event, "| creator:", creator, end=' | ')
    if target is not None:
        print("target:", target, end =' | ')
    if outcome is not None:
        print("result:", outcome, end=' | ')
    print('\n', end=None)


# puts an embed in the text chat to kick a member of the voice chat
@tree.command(name="vote_kick", description="vote to kick from call")
async def vote_kick(interaction, target: discord.Member):
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

    console_output(event_name, interaction.user.id, target.id, event_result)


@tree.command(name="info", description="gives information about the bot")
async def info(interaction):
    """
    sends information on the bot to the invoker
    :return: none
    """
    embed = discord.Embed(title="UwU Bot", description=VERSION)
    embed.add_field(name="Lead Dev:", value="⠀⠀SpySandwiches")
    await interaction.response.send_message(embed=embed)


@tree.command(name="patch", description="shows the latest patch notes")
async def patch(interaction):
    """
    Shows the latest patch from readme.md
    :return: none
    """
    embed = discord.Embed(title="UwU Bot", description="UwU bot (internally NUwU) is my personal discord bot")
    with open("readme.md") as infile:
        for line in infile:
            # skips title and description, as they have to be set on initialization of the embed object
            if line == "# UwU bot\n" or line == "UwU bot (internally NUwU) is my personal discord bot\n":
                pass
            # adds version label to the name of the field instead of the value, makes it slightly larger
            elif line[0] == '#':
                embed.add_field(name=line, value="", inline=False)
            else:
                embed.add_field(name="", value=line, inline=False)

    await interaction.response.send_message(embed=embed)


# on ready
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for femboys OwO"))

client.run("secret")


