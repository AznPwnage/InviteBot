import discord
from discord import app_commands

from main import bot
from src.business.OAuthTokenHandler import get_oauth_token
from src.dao.InviteDao import send_invite
from src.dao.MembershipIdDao import get_membership_id
from src.enums.Clans import Clans
from src.enums.MembershipTypes import MembershipTypes


@bot.tree.command()
@app_commands.rename(bungie_name='bungie-name')
@app_commands.rename(membership_type='platform')
@app_commands.describe(
    bungie_name='Bungie Name of the user to invite (include the # and numbers)',
    membership_type='Platform',
    clan='Name of clan',
)
async def invite(interaction: discord.Interaction, bungie_name: str, membership_type: MembershipTypes, clan: Clans):
    """Invite a user to the clan"""
    try:
        oauth_token = get_oauth_token(clan)
    except Exception:
        await interaction.response.send_message('Unable to fetch token for ' + clan.name + ' please reauthenticate.')
        return

    try:
        membership_id = get_membership_id(bungie_name, membership_type.value)
    except Exception:
        await interaction.response.send_message('Unable to find membership id for ' + bungie_name + '.')
        return

    try:
        send_invite(membership_type.value, membership_id, clan.value, oauth_token.access_token)
    except Exception:
        await interaction.response.send_message('Unable to send invite to ' + bungie_name + ' for ' + clan.name + '.')
        return

    await interaction.response.send_message(bungie_name + ' invited to ' + clan.name + '.')
