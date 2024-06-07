from discord.ext import commands
from main import __version__
from utils import *
import discord

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def help(self, ctx):
        prefix = self.client.command_prefix
        embed = discord.Embed(title=f"**- Help Page -**", color=discord.Color.green())
        embed.add_field(name=f"{prefix}redditpost",value="Taking post from reddit",inline=False)
        embed.add_field(name=f"{prefix}addsub",value="Adding listener subreddit for channel (admin only)",inline=False)
        embed.add_field(name=f"{prefix}delsub",value="Deleting listener subreddit from channel (admin only)",inline=False)
        embed.add_field(name=f"{prefix}checksub",value="Shows data for channels that have a listener (admin only)",inline=False)
        embed.add_field(name=f"{prefix}help",value="Show help commands",inline=False)
        embed.add_field(name=f"{prefix}credits",value="Show credits",inline=False)
        embed.set_footer(text=f"Bot Version: **{__version__}**")
        await ctx.send(embed=embed)
    
    @commands.command(name="credits")
    async def credits(self, ctx):
        embed = discord.Embed(title=f"**- Credits -**", color=discord.Color.green())
        embed.add_field(name=f"Owca525: Creator",value="Github: https://github.com/Owca525",inline=False)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(utils(client))
    logger.info("Utils is online")