import discord
from discord import app_commands
from discord.ext import commands

from src.constants.Constants import DEV_CHANNEL_ID
from src.utils.GuildUtils import get_guild_by_id


class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def sync(self,
                   interaction: discord.Interaction,
                   guild_id: str):
        if interaction.channel_id == DEV_CHANNEL_ID:
            tree = self.bot.tree
            guild = discord.Object(id=guild_id)

            await interaction.response.defer()

            tree.copy_global_to(guild=guild)
            await tree.sync(guild=guild)

            with open('resources/obws_clear.png', 'rb') as image:
                await self.bot.user.edit(avatar=image.read())

            guild = get_guild_by_id(self.bot, int(guild_id))
            await guild.get_member(self.bot.user.id).edit(nick="The Obsidian Watcher")
            await interaction.followup.send('Synced.')
        else:
            await interaction.response.send_message('Wrong channel.')
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SyncCog(bot))
