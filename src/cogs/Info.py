import discord
from discord import app_commands
from discord.ext import commands


class ClanInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="claninfo",
        description="Provide clan info."
    )
    async def claninfo(self,
                       interaction: discord.Interaction):
        await interaction.response.defer()

        


async def setup(bot):
    await bot.add_cog(ClanInfoCog(bot))
