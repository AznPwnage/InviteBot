import csv
from io import StringIO
import pandas as pd

import discord
import requests
from discord import app_commands
from discord.ext import commands

from src.constants.Constants import OBSIDIAN_WATCHERS_MEMBER_ROLE
from src.utils.GuildUtils import get_member, get_guild_members_by_role, get_role_by_name, \
    get_guild_members_by_role_name


class RoleContextCog(commands.Cog):
    clan_score_roles = []
    clan_score_roles_by_name = {}
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

        get_member_fail_count = 0
        update_role_fail_count = 0
        update_role_success_count = 0

        attachment_url = message.attachments[0].url
        file_request = requests.get(attachment_url)
        role_file = StringIO(file_request.text)

        guild_members_with_clan_role = get_guild_members_by_role_name(interaction, OBSIDIAN_WATCHERS_MEMBER_ROLE)
        df = pd.read_csv(role_file)

        self.load_clan_score_roles(interaction)
        for clan_score_role in self.clan_score_roles:
            guild_members_with_score_role = get_guild_members_by_role(clan_score_role)

            for member in guild_members_with_score_role:
                if member in guild_members_with_clan_role:
                    row = df.loc[df.iloc[:, 0] == member.nick]
                    if row and row[1] != clan_score_role.name:
                        await member.remove_roles(clan_score_role)
                        await member.add_roles(self.clan_score_roles_by_name[row[1]])
                else:
                    await member.remove_roles(clan_score_role)

        response_message = 'Completed updating roles. Updated roles for ' + str(update_role_success_count) + \
                           ' members, failed to update roles for ' + str(update_role_fail_count) + \
                           ' members, failed to get object for ' + str(get_member_fail_count) + ' members.'
        if interaction.is_expired():
            await interaction.channel.send(response_message)
        else:
            await interaction.followup.send(response_message)

    @app_commands.command(
        name='cleanup',
        description='Scans server members and removes clan score roles if not in clan.'
    )
    async def cleanup(self,
                      interaction: discord.Interaction):
        role_remove_fail_count = 0
        role_remove_success_count = 0

        try:
            guild_members_with_clan_role = get_guild_members_by_role_name(interaction, OBSIDIAN_WATCHERS_MEMBER_ROLE)
        except Exception:
            await interaction.followup.send('Failed to get guild members with clan score roles.')
            return

        self.load_clan_score_roles(interaction)

        for clan_score_role in self.clan_score_roles:
            try:
                guild_members_with_score_role = get_guild_members_by_role(clan_score_role)
            except Exception:
                await interaction.followup.send('Failed to get guild members by role.')
                return

            try:
                guild_members_to_cleanup = (list(set(guild_members_with_score_role).difference(set(guild_members_with_clan_role))))
            except Exception:
                await interaction.followup.send('Failed to build list of guild members to clean up.')
                return

            for member in guild_members_to_cleanup:
                try:
                    await member.remove_roles(clan_score_role)
                    role_remove_success_count += 1
                except Exception:
                    role_remove_fail_count += 1

        await interaction.followup.send('Completed role cleanup. Removed roles for ' + str(role_remove_success_count) + ' members, failed to remove roles for ' + str(role_remove_fail_count) + ' members.')

    def load_clan_score_roles(self, interaction: discord.Interaction):
        if not self.clan_score_roles:
            for role_name in self.clan_score_role_names:
                role = get_role_by_name(interaction, role_name)
                if role is not None:
                    self.clan_score_roles.append(role)
                    self.clan_score_roles_by_name[role.name] = role


async def setup(bot):
    await bot.add_cog(RoleContextCog(bot))
