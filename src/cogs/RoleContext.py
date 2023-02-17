import csv
from io import StringIO

import discord
import requests
from discord import app_commands
from discord.ext import commands

from src.constants.Constants import OBSIDIAN_WATCHERS_MEMBER_ROLE
from src.utils.GuildUtils import get_member, get_guild_members, get_guild_members_by_role, get_role_by_name, \
    get_guild_members_by_role_name


class RoleContextCog(commands.Cog):
    clan_score_roles = []
    with open('src/constants/ClanRoles.txt') as file:
        clan_score_role_names = [line.rstrip() for line in file]

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
            self.load_clan_score_roles(interaction)
            for role in self.clan_score_roles:
                await member.remove_roles(role)
            role_to_add = discord.utils.get(interaction.guild.roles, name=row[1])
            await member.add_roles(role_to_add)

        await interaction.followup.send('Success.')

    @app_commands.command(
        name='cleanup',
        description='Scans server members and removes clan score roles if not in clan.'
    )
    async def cleanup(self,
                      interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild_members_with_clan_role = get_guild_members_by_role_name(interaction, OBSIDIAN_WATCHERS_MEMBER_ROLE)
        self.load_clan_score_roles(interaction)
        for clan_score_role in self.clan_score_roles:
            guild_members_with_score_role = get_guild_members_by_role(clan_score_role)
            guild_members_to_cleanup = (list(set(guild_members_with_score_role).difference(set(guild_members_with_clan_role))))
            for member in guild_members_to_cleanup:
                member.remove_roles(clan_score_role)

    def load_clan_score_roles(self, interaction: discord.Interaction):
        if not self.clan_score_roles:
            for role_name in self.clan_score_role_names:
                role = get_role_by_name(interaction, role_name)
                if role is not None:
                    self.clan_score_roles.append(role)


async def setup(bot):
    await bot.add_cog(RoleContextCog(bot))
