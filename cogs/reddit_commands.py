from re import sub
import discord
import praw
import asyncpraw

import random

from discord.ext import commands, tasks 
from discord.ext.commands.bot import Bot
import os

reddit = asyncpraw.Reddit(client_id = os.getenv('R_CLIENT_ID'),
                    client_secret=os.getenv('R_CLIENT_SECRET'),
                    username=os.getenv('R_USERNAME'),
                    password=os.getenv('R_PASSWORD'),
                    user_agent='bot_name')

# The "world_news" command can be reused to create custom standalone commands for any desired subreddit
# Note that each command/subreddit needs its own buffer to store the posts

#---------buffers-----------#
all_worldnews_submissions = []
dynamicbuffer = []
dynamicname = ""

@commands.Cog.listener()
async def on_ready():
    clear_submissions.start()

@tasks.loop(minutes=45)
async def clear_submissions():
    all_worldnews_submissions.clear()
    dynamicbuffer.clear()

async def get_buffer(subname, buffer):
    subreddit = await reddit.subreddit(subname) 
    if(len(buffer) == 0):
        top = subreddit.hot(limit=50)
        async for sub in top:
            buffer.append(sub) 
    random_post = random.choice(buffer)
    name = random_post.title
    url = random_post.url
    text = random_post.selftext
    return name, url, text

async def get_dynamic(sub):
    name, url, text = await get_buffer(sub, dynamicbuffer)
    return name, url, text 

async def get_worldnews():
    name, url, text = await get_buffer('worldnews', all_worldnews_submissions)
    return name, url, text

class reddit_commands(commands.Cog,name='reddit'):
    def __init__(self,bot):
        self.bot = bot
        self.description='Browse pre-defined subreddits'

    @commands.command(help="Enter a custom subreddit. By using the command again without a specified subreddit (.browse), you'll get another post from the previously specified subreddit")
    async def browse(self,ctx, subreddit_name=None): 
        if(subreddit_name is None): #if no sub specified, check if earlier there was a specified sub
            if(len(dynamicbuffer) == 0): #if not, return
                await ctx.send("No previously stored subreddit available. Please enter a new subreddit to browse")
            else:  #else, provide another post from earlier su b
                await subredditsearch(ctx, self.next_dynamic)
                self.next_dynamic = await get_dynamic(self.dynamicname)
        else: #if new sub specified, override old buffer and name
            self.dynamicname = subreddit_name
            dynamicbuffer.clear()
            self.next_dynamic = await get_dynamic(subreddit_name)
            try:
                await subredditsearch(ctx, self.next_dynamic)
            finally: 
                self.next_dynamic = await get_dynamic(subreddit_name)

    @commands.command()
    async def worldnews(self,ctx):
        if not hasattr(self, 'next_worldnews_post'):
            self.next_worldnews_post = await get_worldnews()
        await subredditsearch(ctx, self.next_worldnews_post)
        self.next_worldnews_post = await get_worldnews()

    
async def subredditsearch(ctx, buffername): 
        name, url, text = buffername
        embedded_post = discord.Embed(title = name)
        embedded_post.set_image(url = url) 
        if(not (text == "" or text is None)):
            firsttext = text[:1019]
            if(text[1019:] != ''):
                firsttext = firsttext + "[...]"
            embedded_post.add_field(name="Text of the post:",value=firsttext)
        embedded_post.add_field(inline=False,name="NOTE:",value=f'If something doesn\'t load, it\'s probably a video. [Click Here]({url})')
        await ctx.send(embed = embedded_post)
        
async def setup(bot): 
    await bot.add_cog(reddit_commands(bot))