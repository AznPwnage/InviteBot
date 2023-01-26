import discord
from discord import app_commands
from discord.ext import commands

from src.business.OAuthTokenHandler import convert_response_to_oauth_token, save_oauth_token
from src.dao.OAuthTokenDao import call_oauth_token_api
from src.enums.Clans import Clans
from src.enums.GrantTypes import GrantTypes


class AuthorizeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def authorize(self,
                        interaction: discord.Interaction,
                        name: str = commands.param(description='Name of account'),
                        clan: Clans = commands.param(description='Name of clan'),
                        code: str = commands.param(description='Code copied from URL')):
        """Authorize the bot to use your Bungie account"""

        try:
            response = call_oauth_token_api(code, GrantTypes.AuthorizationCode.value)
        except Exception:
            await interaction.response.send_message('Failed to authorize ' + name + ' for ' + clan.name + '.')
            return

        oauth_token = convert_response_to_oauth_token(response.json())
        save_oauth_token(clan, oauth_token)

        await interaction.response.send_message(name + ' authorized for ' + clan.name + '.')


def setup(bot):
    bot.add_cog(AuthorizeCog(bot))
