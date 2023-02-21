from typing import List

import discord
from discord.ext import commands

from src.constants.Constants import BETA_GUILD_ID, DEV_GUILD_ID, REGISTERED_USER_ROLE_NAME


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
    return guild_id != DEV_GUILD_ID


def is_registered_user(roles: List[discord.Role]):
    return any(role.name == REGISTERED_USER_ROLE_NAME for role in roles)


def get_member(bot: commands.bot, interaction: discord.Interaction, bungie_name: str):
    guild = get_guild(bot, interaction)
    return discord.utils.get(guild.members, nick=bungie_name)


def get_guild_member_names(bot: commands.bot, interaction: discord.Interaction):
    guild = get_guild(bot, interaction)
    guild_member_names = []
    for member in guild.members:
        if member.nick is not None:
            guild_member_names.append(member.nick)
    return guild_member_names


def get_guild_members(bot: commands.bot, interaction: discord.Interaction):
    guild = get_guild(bot, interaction)
    guild_members = []
    for member in guild.members:
        guild_members.append(member)
    return guild_members


def get_guild_members_by_role(role: discord.Role):
    return role.members


def get_guild_members_by_role_name(interaction: discord.Interaction, role_name: str):
    role = get_role_by_name(interaction, role_name)
    return get_guild_members_by_role(role)


def get_role_by_name(interaction: discord.Interaction, role_name: str) -> discord.Role:
    return discord.utils.get(interaction.guild.roles, name=role_name)


async def validate_bungie_name(interaction, bungie_name):
    try:
        if bungie_name is None:
            await interaction.followup.send('Invalid nickname for user, please set server nickname to match bungie name.')
            return
    except Exception:
        await interaction.followup.send('Error while validating bungie name.')
    return
