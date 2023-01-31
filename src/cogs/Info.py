import discord
from discord import app_commands
from discord.ext import commands

from src.business.InfoHandler import get_divisions_info_by_region
from src.dao.ClanInfoDao import get_clan_info


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="divisioninfo",
        description="Provide member count & status of OBWS divisions."
    )
    async def divisioninfo(self,
                          interaction: discord.Interaction):
        await interaction.response.defer()

        clan_info_dict = get_clan_info()
        divisions_by_region = get_divisions_info_by_region(clan_info_dict)

        embed = discord.Embed(title="Obsidian Watchers <:OBWS_Clan:885217965316898827>: Divisions Info", color=0x68469c)
        for k, v in divisions_by_region.items():
            embed.add_field(name=k, value=v, inline=True)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(InfoCog(bot))
