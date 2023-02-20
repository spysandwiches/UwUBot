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
