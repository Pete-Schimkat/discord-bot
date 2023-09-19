import asyncio
import aiohttp
import discord
import random
from asyncio.tasks import sleep
from discord.ext import commands , tasks
import os 
import contextlib
from dotenv import load_dotenv
import dotenv
import datetime
import os

intents = discord.Intents.default()
intents.members=True 
intents.messages=True
intents.members=True
intents.message_content=True

location = ['in Berlin',
    'at home']

activity = ['card games',
    'Monopoly',
    'Scrabble']

channel_id = os.getenv("CHANNEL_ID")

class MyBot(commands.Bot):

    async def setup_hook(self) -> None:
        await bot.load_extension('cogs.soundboard_commands')
        await bot.load_extension('cogs.music_commands')
        await bot.load_extension('cogs.basic_commands')
        await bot.load_extension('cogs.reddit_commands')
        await bot.load_extension('cogs.weather_commands')
        bot.session = aiohttp.ClientSession()

bot=MyBot(command_prefix=".", intents=intents)

load_dotenv()

@bot.event
async def on_ready(): 
    change_status.start()
    print('Setup finished.')

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    await bot.process_commands(msg)
    

    
@tasks.loop(minutes=60)
async def change_status():
    await bot.change_presence(activity=discord.Game(f'{random.choice(activity)} {random.choice(location)}'))

@bot.event
async def on_member_join(member): 
    channel = bot.get_channel(channel_id)
    await channel.send(f'Welcome {member.name} :)')
    
@bot.event
async def on_member_remove(member): 
    channel = bot.get_channel(channel_id)
    await channel.send(f'Goodbye {member.name} :(')

# Help-Command Source: https://github.com/JDsProjects/JDJGBotSupreme/blob/97b603aaf9d8391c43c2392ccf33967b8c84b608/cogs/help.py

class HelpEmbed(discord.Embed): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [Category] for more information | <> is required | [] is optional"
        self.set_footer(text=text)
        self.color = discord.Color.blurple()


class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__( 
            command_attrs={
                "help": "Help command for the bot",
                "aliases": ['commands']
            }
        )
    
    async def send(self, **kwargs):
        """a short cut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """triggers when a `<prefix>help` is called"""
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        embed.set_thumbnail(url=ctx.me.avatar.url)
        usable = 0 
        for cog, commands in mapping.items(): 
            if filtered_commands := await self.filter_commands(commands): 
                amount_commands =  len(filtered_commands)
                usable += amount_commands
                if cog: 
                    name = cog.qualified_name
                    description = cog.description or "-----"
                embed.add_field(name=f"{name} [{amount_commands}]", value=description)
        embed.description = f"{len(bot.commands)} commands" #| {usable} usable" 
        await self.send(embed=embed)

    async def send_command_help(self, command):
        signature = self.get_command_signature(command) # get_command_signature gets the signature of a command in <required> [optional]
        embed = HelpEmbed(title=signature, description=command.help or "No Help available :(")

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        can_run = "No"
        # command.can_run to test if the cog is usable
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"
            
        embed.add_field(name="Usable", value=can_run)

        if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await self.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = HelpEmbed(title=title, description=description or "No Help available :(")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No Help available :(")
           
        await self.send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "No "
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())
        

bot.help_command = MyHelp()

bot.run(os.getenv('DISCORD_TOKEN'))
