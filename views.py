import discord


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
        super().__init__()
        self.player_choice = None  # stores player choice
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
    @discord.ui.button(label="Rock", style=discord.ButtonStyle.blurple, emoji="🪨")
    async def rock_button(self, interaction, button: discord.ui.Button):
        self.player_choice = self.choices[0]

    # Paper button
    @discord.ui.button(label="Paper", style=discord.ButtonStyle.blurple, emoji="🗒️")
    async def paper_button(self, interaction, button: discord.ui.Button):
        self.player_choice = self.choices[1]

    # Scissor button
    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.blurple, emoji="✂️")
    async def scissor_button(self, interaction, button: discord.ui.Button):
        self.player_choice = self.choices[2]

