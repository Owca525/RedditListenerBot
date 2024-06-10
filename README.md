# RedditListenerBot
A simple bot made using the script I created and sending content to Discord channels.
It was created because someone asked me to make it for r/hentai
# How To Work
It creates a database by default in ./db and a file called reddit.db, where it stores data such as who did what, etc. It checks the entire database approximately every 4 minutes, makes a request to Reddit, and sends things that have changed, and so on
# Commands
Default prefix is ?
- `redditpost` Taking post from reddit
- `addsub` Adding listener subreddit for channel (admin only)
- `delsub` Deleting listener subreddit from channel (admin only)
- `checksub` Shows data for channels that have a listener (admin only)
- `help` Show help commands
- `credits` Show credits
  For Owner bot
- `sendlog` Sending log
- `ping` Show Latency bot
- `reload` Reloading all cogs
- `devinfo` Show all info bot
# Requirements
- [Python](https://www.python.org/) 3.9-3.12
- [python-dotenv](https://pypi.org/project/python-dotenv/) 1.0.1
- [discord.py](https://pypi.org/project/discord.py/) 2.3.2
- [asyncio](https://pypi.org/project/asyncio/) 3.4.3
- [httpx](https://www.python-httpx.org/) 0.27.0
# Credits
Owca525: Creator
