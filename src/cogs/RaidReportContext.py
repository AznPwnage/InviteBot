import discord
from discord import app_commands
from discord.ext import commands

from src.dao.MembershipIdDao import get_membership_id_and_membership_type
from src.enums.MembershipTypes import MembershipTypes
from src.utils.GuildUtils import validate_user_roles, validate_bungie_name


class RaidReportContextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Raid Report',
            callback=self.raid_report_context
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def raid_report_context(self,
                                  interaction: discord.Interaction,
                                  message: discord.Message):
        await interaction.response.defer(ephemeral=True)
        member = message.author
        bungie_name = member.nick

        await validate_user_roles(interaction, member)
        await validate_bungie_name(interaction, bungie_name)

        try:
            membership_id, membership_type = get_membership_id_and_membership_type(bungie_name)
        except Exception:
            await interaction.followup.send('Unable to find membership id for ' + bungie_name + '.')
            return

        await interaction.followup.send(self.construct_raid_report_link(membership_id, membership_type))

    def construct_raid_report_link(self, membership_id, api_membership_type):
        rr_membership_type_code = self.get_rr_membership_type_code(api_membership_type)
        return 'https://www.raid.report/' + rr_membership_type_code + '/' + membership_id

    def get_rr_membership_type_code(self, api_membership_type):
        for membership_type in MembershipTypes:
            if membership_type.value.code == api_membership_type:
                return membership_type.value.rr_code


async def setup(bot):
    await bot.add_cog(RaidReportContextCog(bot))
