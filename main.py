from discord.ext import commands, tasks
from dotenv import load_dotenv
from utils import *
import datetime
import asyncio
import discord
import ast
import os

__version__ = "1.0"
__location_database__ = "./db/"
__name_database__ = "reddit.db"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(
    command_prefix="?",
    help_command=None,
    intents=discord.Intents.default()
)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Uknown Command please type help")
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send(":no_entry_sign: You don't have permision :no_entry_sign: ")
        return
    
    logger.error(error)

@client.event
async def on_ready():
    for filename in os.listdir('./cogs'):
         if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
            except Exception as error:
                logger.critical(f'{error}')

    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.activity.Game(f"My prefix is {client.command_prefix}")
    )

    await client.wait_until_ready() 
    logger.info(f'Connected To {client.user.name}')
    await reddit_background_task.start()

async def send(channel, data):
    channel = client.get_channel(channel)
        
    for item in data:
        gallery = re.findall(r'(?:https?:\/\/)?(?:www\.|old\.|i\.|new\.)?(?:reddit\.com|redd\.it)\/(?:r\/[^\s\/$.?#]+\/)?gallery\/',item[0])

        if gallery != []:
            sub = await post_grabber.grabber(url=item[0],subreddit=re.findall(r'(?:https?:\/\/)?(?:www\.|old\.|i\.|new\.)?(?:reddit\.com|redd\.it)\/(?:r\/([^\s\/$.?#]+)\/comments\/|gallery\/)([^\s\/$.?#]+)', item[1])[0])
            for i,item2 in enumerate(sub):
                embed_message = discord.Embed(title=f"From Reddit: {item[1].replace('old.reddit.com','www.reddit.com')}", color=discord.Color.orange(),description=f"{item[2]}")
                embed_message.set_image(url=item2).set_footer(text=f"image {i+1}/{len(sub)}")
                await channel.send(embed=embed_message)
                await asyncio.sleep(0.7)

        if gallery == []:
            embed_message = discord.Embed(title=f"From Reddit: {item[1].replace('old.reddit.com','www.reddit.com')}", color=discord.Color.orange(),description=f"{item[2]}")
            embed_message.set_image(url=item[0]).set_footer(text=f"post 1/1")
            await channel.send(embed=embed_message)
            await asyncio.sleep(1)

tmp_url = []
tmp_post = []

async def check_tmp(url):
    return tmp_url.index(url) if url in tmp_url else ""

async def set_data(data):
    tmp_checked = await check_tmp(data[4])
    if tmp_checked != "":
        await update_data(data[1], "last_check",str(tmp_post[tmp_checked]),data[4])
        await update_data(data[1], "last_check_timestamp",str(datetime.datetime.now()),data[5])
        await send(data[0],[item for item in tmp_post[tmp_checked] if item not in ast.literal_eval(data[5])])
        return

    sub = await subreddit_grabber.grabber(data[4])
    if sub != []:
        await update_data(data[1], "last_check",str(sub),data[5])
        await update_data(data[1], "last_check_timestamp",str(datetime.datetime.now()),data[6])

        tmp_url.append(data[4])
        tmp_post.append(sub)
        await send(data[0],[item for item in sub if item not in ast.literal_eval(data[5])])
    else:
        logger.error(f"Extracting error: {data[4]}")
    
    return

@tasks.loop(seconds=300)
async def reddit_background_task():
    logger.info("Running Task: Reddit")
    tmp_url.clear()
    tmp_post.clear()
    try:
        conn = await create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = sum([await get_all_data(str(item[0][1:])) for item in cursor.fetchall()], [])
        for item in data:
            await set_data(item)
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    if os.path.exists(__location_database__) != True:
        os.mkdir(__location_database__)
    
    if os.path.exists(__location_database__ + __name_database__) != True:
        logger.info("Creating database")
        conn = create_connection()
        conn.close()

    if TOKEN == None:
        logger.error("Token no find")
        exit()

    try:
        client.run(TOKEN)
    except Exception as e:
        logger.error(e)