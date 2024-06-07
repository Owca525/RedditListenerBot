from discord.ext import commands
from discord.ui import View
from utils import *
import datetime
import discord
import re

class PaginationView(View):
    def __init__(self, post: list, url: str, title: str):
        super().__init__()
        self.current_page = 0
        self.post = post
        self.url = url
        self.title = title

    async def create_embed(self, post):
        embed_message = discord.Embed(title=f"From Reddit: {self.url.replace('old.reddit.com','www.reddit.com')}", color=discord.Color.orange(), description=str(self.title))
        embed_message.set_image(url=post[self.current_page]).set_footer(text=f"post {self.current_page+1}/{len(self.post)}")
        return embed_message

    async def send_with_pagination(self, ctx):
        embed = await self.create_embed(self.post)

        if isinstance(embed, str) != True:
            self.message = await ctx.send(embed=embed, view=self)
        else:
            self.message = await ctx.send(embed, view=self)
        
    async def send_multiply(self,post):
        embed = await self.create_embed(post)

        if isinstance(embed, str) != True:
            await self.message.edit(embed=embed, view=self)
        else:
            await self.message.edit(content=str(embed))

    @discord.ui.button(label="<-", style=discord.ButtonStyle.green)
    async def prevButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        if str(self.current_page).find("-") != -1:
            self.current_page += 1

        await self.send_multiply(self.post)

    @discord.ui.button(label="->", style=discord.ButtonStyle.green)
    async def nextButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        if self.current_page > len(self.post):
            self.current_page -= 1

        await self.send_multiply(self.post)

class reddit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="redditpost")
    async def redditpost(self, ctx, url: str):
        if re.findall(r'^(https?:\/\/)?(www\.|old\.|i\.|new\.)?(reddit\.com|redd\.it)\/[^\s\/$.?#].[^\s]*$',str(url)) == []:
            await ctx.send("Wrong post")
            return

        post = await post_grabber.grabber(url=url,subreddit=re.findall(r'(?:https?:\/\/)?(?:www\.|old\.|i\.|new\.)?(?:reddit\.com|redd\.it)\/(?:r\/([^\s\/$.?#]+)\/comments\/|gallery\/)([^\s\/$.?#]+)', url)[0])
        if len(post[0]) == 1:
            embed_message = discord.Embed(title=f"From Reddit: {url.replace('old.reddit.com','www.reddit.com')}", color=discord.Color.orange(), description=str(post[1]))
            embed_message.set_image(url=url).set_footer(text=f"post 1/1")
            await ctx.send(embed=embed_message)
            return
        
        if len(post[0]) > 1:
            await PaginationView(
                post=post[0],
                url=url,
                title=post[1]
            ).send_with_pagination(ctx)
            return

        await ctx.send("Nothing found")

class redditlistenercommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="addsub")
    @commands.has_permissions(administrator=True)
    async def addsub(self, ctx, channel, url):
        if re.findall(r'https?://(?:www|i|new)\.reddit\.com/r/Nekomimi/(?:top|new|controversial|rising)/?$',str(url)) == []:
            await ctx.send("Wrong subreddit")
            return
        
        conn = https()
        await conn.get(url)
        if conn.status in [404,301,300]:
            await ctx.send("Something wrong with this subreddit")
            return 

        try:
            if self.client.get_channel(int(re.findall(r'<#(\d+)>', channel)[0])):
                conn = await create_connection()
                await create_tables(conn, f"{ctx.guild.id}")
                sub = subreddit_grabber()
                sub.grabber(url)
                await add_data(conn, ctx.guild.id, (re.findall(r'<#(\d+)>', channel)[0], ctx.guild.id, ctx.author.id, datetime.datetime.now(), url, str(sub.posts), datetime.datetime.now()))
                conn.close()

                await ctx.send(f":white_check_mark: Successfully added subreddit: {url} for channel: {channel}")
        except IndexError:
            await ctx.send(":x: This channel dosen't exist :x: ")

    @commands.command(name="delsub")
    @commands.has_permissions(administrator=True)
    async def delsub(self, ctx, channel):
        try:
            if self.client.get_channel(int(re.findall(r'<#(\d+)>', channel)[0])):
                conn = await create_connection()
                await delete_data(conn, ctx.guild.id, re.findall(r'<#(\d+)>', channel)[0])
                await ctx.send(f":white_check_mark: Successfully deleted subreddit from {channel}")
                conn.close()
        except IndexError:
            await ctx.send(":x: This channel dosen't exist :x: ")

    @commands.command(name="checksub")
    @commands.has_permissions(administrator=True)
    async def checksub(self, ctx):
        conn = await create_connection()
        data = await get_data(conn, ctx.guild.id)
        conn.close()

        if data == []:
            await ctx.send("Nothing added")
            return
        
        embed_message = discord.Embed(title=f"Subbreddit added in the channels:", color=discord.Color.orange())
        for item in data:
            embed_message.add_field(name=f'#{self.client.get_channel(item[0])} on {item[2][:item[2].rfind(".")]}',value=f"Subreddit: {item[3]}",inline=False)

        await ctx.send(embed=embed_message)

async def setup(client):
    await client.add_cog(redditlistenercommands(client))
    await client.add_cog(reddit(client))
    logger.info("Reddit is online")
