import discord
from discord import app_commands
from discord.ext import commands

from src.constants.Constants import DEV_CHANNEL_ID


class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def sync(self,
                   interaction: discord.Interaction):
        if interaction.channel_id == DEV_CHANNEL_ID:
            tree = self.bot.tree
            guild = interaction.guild

            await interaction.response.defer()

            tree.copy_global_to(guild=guild)
            await tree.sync(guild=guild)
            await interaction.followup.send('Synced.')
        else:
            await interaction.response.send_message('Wrong channel.')
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SyncCog(bot))
