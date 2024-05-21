import discord
from discord import app_commands
from discord.ext import commands

from src.constants.Constants import OBSIDIAN_WATCHERS_MEMBER_ROLE, SERVER_MEMBER_ROLE, PURGE_SURVIVOR_ROLE
from src.utils.GuildUtils import get_guild_members, get_guild_members_by_role_name


class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="purge",
        description="Scans server members and kicks members lacking certain roles"
    )
    async def purge(self,
                    interaction: discord.Interaction):
        await interaction.response.defer()

        success_count = 0
        fail_count = 0

        try:
            guild_members = get_guild_members(interaction)
        except Exception:
            await interaction.followup.send('Failed to get server member role list')
            return

        try:
            guild_members_with_purge_survivor_role = get_guild_members_by_role_name(interaction, PURGE_SURVIVOR_ROLE)
        except Exception:
            await interaction.followup.send('Failed to get purge survivor member role list')
            return

        try:
            guild_members_with_clan_member_role = get_guild_members_by_role_name(interaction,
                                                                                 OBSIDIAN_WATCHERS_MEMBER_ROLE)
        except Exception:
            await interaction.followup.send('Failed to get clan member role list')
            return

        try:
            guild_members_to_purge = (list(
                set(guild_members).difference(set(guild_members_with_purge_survivor_role))))
        except Exception:
            await interaction.followup.send('Failed to remove purge survivors')
            return

        try:
            guild_members_to_purge = (
                list(set(guild_members_to_purge).difference(set(guild_members_with_clan_member_role))))
        except Exception:
            await interaction.followup.send('Failed to remove clan members')
            return

        for member in guild_members_to_purge:
            try:
                await member.kick()
                success_count += 1
            except Exception:
                fail_count += 1

        await interaction.followup.send(
            'Completed purge. Kicked ' + str(success_count) + ' members, failed to kick ' + str(
                fail_count) + ' members.')


async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
