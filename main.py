import discord
import asyncio
import time
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# View object for vote_kick (contains buttons)
class KickButtons(discord.ui.View):
    def __init__(self, eligible_ids):
        super().__init__()
        self.yesVotes = 0
        self.noVotes = 0
        self.voteIDs = [0]
        self.eligibleIDs = eligible_ids

    # yes button
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_kick_button(self, interaction, button: discord.ui.Button):
        # checks if user is in the voice call with the vote starter
        if interaction.user.id not in self.eligibleIDs:
            await interaction.response.send_message("You're not in that voice channel >:(", ephemeral=True)
        # checks if the user has already voted
        elif interaction.user.id not in self.voteIDs:
            self.yesVotes += 1
            self.voteIDs.append(interaction.user.id)
            await interaction.response.defer()

    # no button
    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_kick_button(self, interaction, button: discord.ui.button):
        # checks if user is in the voice call with the vote starter
        if interaction.user.id not in self.eligibleIDs:
            await interaction.response.send_message("You're not in that voice channel >:(", ephemeral=True)
        # checks if the user has already voted
        elif interaction.user.id not in self.voteIDs:
            self.noVotes += 1
            self.voteIDs.append(interaction.user.id)
            await interaction.response.defer()


# puts an embed in the text chat to kick a member of the voice chat
@tree.command(name="vote_kick", description="vote to kick from call")
async def vote_kick(interaction, target: discord.Member):
    current_channel = interaction.user.voice  # shortcut to voice channel of vote starter
    current_voice_members = []  # stores a snapshot of the voice channel members at the time of the vote
    start_time = 0  # starting time of the vote

    if current_channel is None:
        await interaction.response.send_message("You're not in a voice channel :(", ephemeral=True)
        return 0

    # stores current members of voice channel
    for member in current_channel.channel.members:
        current_voice_members.append(member.id)
    view = KickButtons(current_voice_members)

    # checks if the targeted user is in the voice call
    if target.id not in current_voice_members:
        await interaction.response.send_message("That person isn't in your call :3", ephemeral=True)
        return 0

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
        await target.move_to(None)
        await interaction.edit_original_response(content="Ok, kicked " + target.display_name + \
                                                         "\n Yes: " + str(view.yesVotes) + \
                                                         " | No: " + str(view.noVotes), view=None)
    else:
        await interaction.edit_original_response(content="Vote kick on " + target.display_name + " failed" \
                                                         "\n Yes: " + str(view.yesVotes) + \
                                                         " | No: " + str(view.noVotes), view=None)


# on ready
@client.event
async def on_ready():
    await tree.sync()

client.run("ODk2NTk5ODAwNjU1NTE1NjQ4.GlmKfY.Minv8lLAnIswzPPaGssj9S7F7xd4Jmex3XDH3Q")


