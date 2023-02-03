from typing import List

import discord
from discord.ext import commands

from src.constants.Constants import BETA_GUILD_ID, DEV_GUILD_ID, REGISTERED_USER_ROLE_ID


def get_guild_by_id(bot: commands.bot, guild_id: int):
    return bot.get_guild(guild_id)


def get_guild(bot: commands.bot, interaction: discord.Interaction):
    guild_id = interaction.guild.id
    return get_guild_by_id(bot, guild_id)


async def validate_user_roles(interaction: discord.Interaction, member):
    if is_prod_guild(interaction.guild_id):
        try:
            if not is_registered_user(member.roles):
                await interaction.followup.send('User is not registered to Charlemagne.')
                return
        except Exception:
            await interaction.followup.send('Issue with fetching roles for user.')
            return
    return


def is_prod_guild(guild_id):
    return guild_id != BETA_GUILD_ID and guild_id != DEV_GUILD_ID


def is_registered_user(roles: List[discord.Role]):
    return any(role.id == REGISTERED_USER_ROLE_ID for role in roles)


def get_member(bot: commands.bot, interaction: discord.Interaction, bungie_name: str):
    guild = get_guild(bot, interaction)
    return discord.utils.get(guild.members, nick=bungie_name)


async def validate_bungie_name(interaction, bungie_name):
    try:
        if bungie_name is None:
            await interaction.followup.send('Invalid nickname for user, please set server nickname to match bungie name.')
            return
    except Exception:
        await interaction.followup.send('Error while validating bungie name.')
        return
    return
