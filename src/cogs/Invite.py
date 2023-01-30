from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from src.business.OAuthTokenHandler import get_oauth_token
from src.dao.InviteDao import send_invite
from src.dao.MembershipIdDao import get_membership_id_and_membership_type
from src.enums.Clans import Clans
from src.utils.GuildUtils import get_guild


class InviteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def bungie_name_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        guild_member_names = self.get_guild_member_names(interaction)
        return [
            app_commands.Choice(name=bungie_name, value=bungie_name)
            for bungie_name in guild_member_names if current.lower() in bungie_name.lower()
        ]

    @app_commands.command(
        name="invite",
        description="Invite a user to the clan")
    @app_commands.describe(
        bungie_name="Bungie Name of the user to invite (include the # and numbers)",
        clan="Name of clan")
    @app_commands.rename(
        bungie_name='bungie-name')
    @app_commands.autocomplete(bungie_name=bungie_name_autocomplete)
    async def invite(self,
                     interaction: discord.Interaction,
                     bungie_name: str,
                     clan: Clans):
        """Invite a user to the clan"""
        await interaction.response.defer()
        try:
            oauth_token = get_oauth_token(clan)
        except Exception:
            await interaction.followup.send('Unable to fetch token for ' + clan.name + ' please reauthenticate.')
            return

        try:
            membership_id, membership_type = get_membership_id_and_membership_type(bungie_name)
        except Exception:
            await interaction.followup.send('Unable to find membership id & membership type for ' + bungie_name + '.')
            return

        try:
            send_invite(membership_type, membership_id, clan.value.group_id, oauth_token.access_token)
        except Exception:
            await interaction.followup.send('Unable to send invite to ' + bungie_name + ' for ' + clan.name + '.')
            return

        try:
            member = self.get_member(interaction, bungie_name)
            await interaction.followup.send(member.mention + ' invited to ' + clan.name + '. Welcome to the clan!')
            return
        except Exception:
            print('Unable to find user by server nickname.')

        await interaction.followup.send(bungie_name + ' invited to ' + clan.name + '.')
        return

    def get_member(self, interaction: discord.Interaction, bungie_name: str):
        guild = get_guild(self.bot, interaction)
        return discord.utils.get(guild.members, nick=bungie_name)

    def get_guild_member_names(self, interaction: discord.Interaction):
        guild = get_guild(self.bot, interaction)
        guild_member_names = []
        for member in guild.members:
            if member.nick is not None:
                guild_member_names.append(member.nick)
        return guild_member_names


async def setup(bot):
    await bot.add_cog(InviteCog(bot))
