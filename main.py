from typing import Optional, Literal

import discord
import os

from discord.ext import commands
from discord.ext.commands import Context, Greedy
from dotenv import load_dotenv

load_dotenv('src/config/.env')
token = os.getenv('TOKEN')
beta_guild = discord.Object(id=1066525478887899226)  # replace with your guild id
dev_guild = discord.Object(id=889991299904716830)  # replace with your guild id

initial_extensions = ['src.cogs.Authorize',
                      'src.cogs.Invite']


class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:

        for extension in initial_extensions:
            await self.load_extension(extension)

        if dev_guild:
            self.tree.copy_global_to(guild=dev_guild)
            await self.tree.sync(guild=dev_guild)


bot = CustomBot(activity=discord.Game(name='Destiny 3'), command_prefix='?', intents=discord.Intents.default())


@bot.command()
async def psync(interaction: discord.Interaction):
    bot.tree.copy_global_to(guild=dev_guild)
    await interaction.response.send_message('Sync to dev guild complete.')


@bot.command()
async def bsync(interaction: discord.Interaction):
    bot.tree.copy_global_to(guild=beta_guild)
    await interaction.response.send_message('Sync to beta guild complete.')


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted!')


bot.run(token, reconnect=True)
