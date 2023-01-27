from typing import List

import discord
from discord import app_commands, Role
from discord.ext import commands

from src.business.OAuthTokenHandler import get_oauth_token
from src.constants.Constants import REGISTERED_USER_ROLE_ID, COMMA_DELIMITER
from src.dao.InviteDao import send_invite
from src.dao.MembershipIdDao import get_membership_id
from src.enums.Clans import Clans
from src.enums.MembershipTypes import MembershipTypes


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

        try:
            if not self.is_registered_user(member.roles):
                await interaction.followup.send('User is not registered to Charlemagne.')
                return
        except Exception:
            await interaction.followup.send('Issue with fetching roles for user.')
            return

        try:
            platform, division = self.extract_platform_and_division(message)
        except Exception:
            await interaction.followup.send('Incorrect message format. Please use `<platform>,<division>`.')
            return

        try:
            if not self.validate_platform(platform):
                await interaction.followup.send('Platform is not valid.')
                return
        except Exception:
            await interaction.followup.send('Error while validating platform.')
            return

        try:
            if not self.validate_division(division):
                await interaction.followup.send('Division is not valid.')
                return
        except Exception:
            await interaction.followup.send('Error while validating division.')
            return

        try:
            if not self.validate_bungie_name(member.nick):
                await interaction.followup.send('Invalid nickname for user, please set server nickname to match bungie name.')
                return
        except Exception:
            await interaction.followup.send('Error while validating bungie name.')
            return

        membership_type = MembershipTypes[platform]
        clan = Clans[division]
        bungie_name = member.nick

        try:
            oauth_token = get_oauth_token(clan)
        except Exception:
            await interaction.followup.send('Unable to fetch token for ' + clan.name + ' please reauthenticate.')
            return

        try:
            membership_id = get_membership_id(bungie_name, membership_type.value)
        except Exception:
            await interaction.followup.send('Unable to find membership id for ' + bungie_name + '.')
            return

        try:
            send_invite(membership_type.value, membership_id, clan.value, oauth_token.access_token)
        except Exception:
            await interaction.followup.send('Unable to send invite to ' + bungie_name + ' for ' + clan.name + '.')
            return

        await interaction.followup.send(bungie_name + ' invited to ' + clan.name + '.')
        return

    def is_registered_user(self, roles: List[Role]):
        return any(role.id == REGISTERED_USER_ROLE_ID for role in roles)

    def extract_platform_and_division(self, message):
        message_parts = message.content.split(COMMA_DELIMITER)
        platform = message_parts[0].lower()
        division = message_parts[1].lower()
        return platform, division

    def validate_platform(self, platform):
        return platform in MembershipTypes.member_names_

    def validate_division(self, division):
        return division in Clans.member_names_

    def validate_bungie_name(self, bungie_name):
        return bungie_name is not None


async def setup(bot):
    await bot.add_cog(InviteContextCog(bot))
