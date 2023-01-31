from typing import List

import discord
from discord import app_commands, Role
from discord.ext import commands

from src.business.InfoHandler import get_smallest_division_group_id_by_region_name
from src.constants.Constants import REGISTERED_USER_ROLE_ID, BETA_GUILD_ID, DEV_GUILD_ID
from src.dao.InviteDao import send_invite
from src.dao.MembershipIdDao import get_membership_id_and_membership_type
from src.dao.OAuthTokenDao import get_oauth_token
from src.enums.Clans import Clans
from src.enums.Region import Region


class InviteContextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Invite',
            callback=self.invite_context
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def invite_context(self,
                             interaction: discord.Interaction,
                             message: discord.Message):
        """Invite a user to the clan"""
        await interaction.response.defer()
        member = message.author

        if self.is_prod_guild(interaction.guild_id):
            try:
                if not self.is_registered_user(member.roles):
                    await interaction.followup.send('User is not registered to Charlemagne.')
                    return
            except Exception:
                await interaction.followup.send('Issue with fetching roles for user.')
                return

        try:
            division = self.extract_division(message)
        except Exception:
            await interaction.followup.send('No valid division name found in the message.')
            return

        try:
            if not self.validate_bungie_name(member.nick):
                await interaction.followup.send('Invalid nickname for user, please set server nickname to match bungie name.')
                return
        except Exception:
            await interaction.followup.send('Error while validating bungie name.')
            return

        clan = Clans[division]
        bungie_name = member.nick

        try:
            oauth_token = get_oauth_token(clan)
        except Exception:
            await interaction.followup.send('Unable to fetch token for ' + clan.name + ' please reauthenticate.')
            return

        try:
            membership_id, membership_type = get_membership_id_and_membership_type(bungie_name)
        except Exception:
            await interaction.followup.send('Unable to find membership id for ' + bungie_name + '.')
            return

        try:
            send_invite(membership_type, membership_id, clan.value.group_id, oauth_token.access_token)
        except Exception:
            await interaction.followup.send('Unable to send invite to ' + bungie_name + ' for ' + clan.name + '.')
            return

        await interaction.followup.send(member.mention + ' invited to ' + clan.name + '. Welcome to the clan!')
        return

    def is_registered_user(self, roles: List[Role]):
        return any(role.id == REGISTERED_USER_ROLE_ID for role in roles)

    def extract_division(self, message):
        for division_name in Clans.get_clan_names():
            if division_name in message.content.lower():
                return division_name
        for region_name in Region.get_region_names():
            if region_name.lower() in message.content.lower():
                return get_smallest_division_group_id_by_region_name(region_name)
        raise Exception

    def validate_bungie_name(self, bungie_name):
        return bungie_name is not None

    def is_prod_guild(self, guild_id):
        return guild_id != BETA_GUILD_ID and guild_id != DEV_GUILD_ID


async def setup(bot):
    await bot.add_cog(InviteContextCog(bot))
