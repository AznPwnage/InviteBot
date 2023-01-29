import discord
from discord.ext import commands


def get_guild_by_id(bot: commands.bot, guild_id: int):
    return bot.get_guild(guild_id)


def get_guild(bot: commands.bot, interaction: discord.Interaction):
    guild_id = interaction.guild.id
    return get_guild_by_id(bot, guild_id)
