import discord
import time

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


class RPSButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.player_choice = None  # stores player choice
        self.bot_choice = None
        self.choices = ["rock", "paper", "scissors"]  # stores possible choices
        self.win_dict = {  # stores win conditions for all the choices
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        self.icons = {  # stores icons for fancy output
            "rock": "🪨",
            "scissors": "✂️",
            "paper": "🗒️"}

    # Rock button
    @discord.ui.button(label="Rock", style=discord.ButtonStyle.blurple, emoji="🪨", custom_id="rock_button")
    async def rock_button(self, interaction, button: discord.ui.Button):
        self.player_choice = self.choices[0]
        await interaction.response.defer()

    # Paper button
    @discord.ui.button(label="Paper", style=discord.ButtonStyle.blurple, emoji="🗒️", custom_id="paperb_utton")
    async def paper_button(self, interaction, button: discord.ui.Button):
        self.player_choice = self.choices[1]
        await interaction.response.defer()

    # Scissor button
    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.blurple, emoji="✂️", custom_id="scissors_button")
    async def scissor_button(self, interaction, button: discord.ui.Button):
        self.player_choice = self.choices[2]
        await interaction.response.defer()


class RPSRematch(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.clicked = False
        start_time = time.time()

    @discord.ui.button(label="Rematch?", style=discord.ButtonStyle.blurple, custom_id="rematch_button")
    async def rematch_button(self, interaction, button: discord.ui.button):
        self.clicked = True
        await interaction.response.defer()
