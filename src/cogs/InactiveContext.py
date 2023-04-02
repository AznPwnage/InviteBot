import csv
from io import StringIO

import discord
import requests
from discord import app_commands
from discord.ext import commands

from src.constants.Constants import INACTIVE_NOTIFICATION_CHANNEL_NAME
from src.enums.ClanType import ClanType
from src.enums.Clans import Clans
from src.utils.DictUtils import append_obj_to_value_if_key_exists
from src.utils.GuildUtils import get_member, get_channel_by_name


class InactiveContextCog(commands.Cog):
    activity_checks_by_clan_type = {ClanType.REGIONAL: 'gained 500k XP',
                                    ClanType.RAID: 'gained 500k XP and/or completed 3 full raids'}

    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Mention Inactives',
            callback=self.mention_inactives
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def mention_inactives(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)

        get_member_fail_count = 0
        inactive_members = {}

        attachment_url = message.attachments[0].url
        file_request = requests.get(attachment_url)
        inactive_file = StringIO(file_request.text)

        reader = csv.reader(inactive_file, delimiter=',')
        for row in reader:
            bungie_name = row[0]
            clan_name = row[1]
            try:
                member = get_member(self.bot, interaction, bungie_name)
                append_obj_to_value_if_key_exists(inactive_members, clan_name, member)
            except Exception:
                get_member_fail_count += 1

        for k, v in inactive_members.items():
            clan = Clans[k.lower()].value
            if clan.clan_type in self.activity_checks_by_clan_type.keys():
                activity_check_message = self.activity_checks_by_clan_type[clan.clan_type]
                message = k + ' people,  you\'ve been marked by our program as not having ' + activity_check_message + \
                    ' this past week. Please let us know why or fill out an inactive notification if you plan' \
                    ' on being inactive for an extended period, or you will be removed from the clan in 48' \
                    ' hours. If you joined the clan in the past week, let your region head know as you should be' \
                    ' exempt from this check.\n'
                for member in v:
                    message = message + member.mention + ', '
                message = message[:-2]

                channel = get_channel_by_name(self.bot, interaction, INACTIVE_NOTIFICATION_CHANNEL_NAME)
                await channel.send(message)
        await interaction.followup.send('Success.')
        return


async def setup(bot):
    await bot.add_cog(InactiveContextCog(bot))
