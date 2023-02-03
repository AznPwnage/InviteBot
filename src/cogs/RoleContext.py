import csv
from io import StringIO

import discord
import requests
from discord import app_commands
from discord.ext import commands

from src.utils.GuildUtils import get_member


class RoleContextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Update Roles',
            callback=self.update_roles
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def update_roles(self,
                           interaction: discord.Interaction,
                           message: discord.Message):
        await interaction.response.defer(ephemeral=True)

        attachment_url = message.attachments[0].url
        file_request = requests.get(attachment_url)
        role_file = StringIO(file_request.text)

        reader = csv.reader(role_file, delimiter=',')
        for row in reader:
            member = get_member(self.bot, interaction, row[0])
            role = discord.utils.get(interaction.guild.roles, name=row[1])
            await member.add_roles(role)

        await interaction.followup.send('Success.')


async def setup(bot):
    await bot.add_cog(RoleContextCog(bot))
