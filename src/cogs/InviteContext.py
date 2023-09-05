from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from src.business.InfoHandler import get_smallest_division_name_by_region_name
from src.dao.InviteDao import send_invite
from src.dao.MembershipIdDao import get_membership_id_and_membership_type
from src.dao.OAuthTokenDao import get_oauth_token
from src.enums.Clans import Clans
from src.enums.Region import Region
from src.utils.GuildUtils import validate_user_roles, validate_bungie_name


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
        await interaction.response.defer(ephemeral=True)
        member = message.author
        bungie_name = member.nick

        try:
            await validate_user_roles(interaction, member)
        except:
            return

        try:
            division = self.extract_division(message)
        except Exception:
            await interaction.followup.send('No valid division or region name found in the message.')
            return

        try:
            await validate_bungie_name(interaction, bungie_name)
        except:
            return

        clan = Clans[division]

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

        await interaction.followup.send('Invite successful', ephemeral=True)
        await interaction.channel.send(member.mention + ' (bgn: ' + bungie_name + ') invited to ' + clan.name.capitalize() + ' by ' + interaction.user.display_name + '. Welcome to the clan!')
        return

    def extract_division(self, message):
        for division_name in Clans.get_clan_names():
            if division_name in message.content.lower():
                return division_name
        for region_name in Region.get_region_names():
            if region_name.lower() in message.content.lower():
                return get_smallest_division_name_by_region_name(region_name)
        raise Exception


async def setup(bot):
    await bot.add_cog(InviteContextCog(bot))
