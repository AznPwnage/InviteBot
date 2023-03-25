from typing import Optional, Literal

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('src/config/.env')
token = os.getenv('TOKEN')
beta_guild = discord.Object(id=1066525478887899226)  # replace with your guild id
dev_guild = discord.Object(id=889991299904716830)  # replace with your guild id

initial_extensions = ['src.cogs.Authorize',
                      'src.cogs.Invite',
                      'src.cogs.InviteContext',
                      'src.cogs.Sync',
                      'src.cogs.Info',
                      'src.cogs.RaidReportContext',
                      'src.cogs.RoleContext',
                      'src.cogs.InactiveContext']


class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:

        for extension in initial_extensions:
            await self.load_extension(extension)

        if dev_guild:
            self.tree.copy_global_to(guild=dev_guild)
            await self.tree.sync(guild=dev_guild)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = CustomBot(activity=discord.Game(name='Destiny 3'), command_prefix='>?', intents=intents)


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted!')


bot.run(token, reconnect=True)
