from asyncio.tasks import sleep
import discord
from discord import utils
from discord.ext import commands 
import random


class basic_commands(commands.Cog, name='random'):
    def __init__(self,bot):
        self.bot = bot
        self.description = 'basic commands'

    @commands.command(help='Tells you the latency of the bot.')
    async def ping(self, ctx):
        await ctx.send(f'Current Ping: ({round(self.bot.latency * 1000)} ms)')

    @commands.command(help='Makes the bot take a break (does not actually influence functionality)')
    async def chill(self,ctx): 
            await ctx.send(f'Back soon, 5 minutes :)')
            await self.bot.change_presence(status=discord.Status.idle,activity=discord.Game('Daydreaming',use_aliases=True))
            await sleep(300)
            await self.bot.change_presence(status=discord.Status.online,activity=discord.Game(f'Monopoly at home'))

    @commands.command(help='Splits all users in the current VC into 2 teams.')
    async def teams(self,ctx):
        voice_state  = ctx.message.author.voice
        if(voice_state == None): 
            await ctx.send('Du musst in einem voice channel sein um dieses command zu usen')
        else:
            members = ctx.message.author.voice.channel.members
            random.shuffle(members)
            embed = discord.Embed(title='Teams:')
            
            team1 = []
            team2 = []
            for i in range(len(members)):
                if(i%2==1): 
                    team1.append(members[i].mention)
                else:
                    team2.append(members[i].mention)
            response= ''
            for i in range(len(team1)):
                response += (str(i+1)+'. '+team1[i]+'\n')
            embed.add_field(name='Team 1:',value=response)
            response = ''
            for i in range(len(team2)):
                response += (str(i+1) + '. '+team2[i]+'\n')
            embed.add_field(name='Team 2:',value=response)
            await ctx.send(embed=embed)

    @commands.command(name="games", help="Browser games")
    async def games(self,ctx):
        games= ["Codenames: <https://codenames.game/room/create>",
        "Stadt, Land, Fluss: <https://stadtlandflussonline.net/new-game.xhtml>",
        "Gartic Phone: <https://garticphone.com/de>",
        "Skribbl.io: <https://skribbl.io/>",
        "Uno, Monopoly, Poker, etc.: <https://play.gidd.io>"]
        ret = ""
        for g in games:
            ret = ret + str(g) + "\n"
        await ctx.send(ret)
    
    @commands.command(name ='d',help='roll a custom dice.',aliases = ['dice'])
    async def d(self,ctx, number :int):
        result = random.randint(1,number)
        await ctx.send(f'You rolled a {result}')

    # The following command can be repurposed to send useful images that are needed regularly (e.g. Cheatsheets).
    @commands.command(help="Send a predefined image to the textchannel.")
    async def image(self,ctx): 
        await ctx.send(file=discord.File("./image_name.png"))

    # This command can be repurposed to create more commands for links that are regularly needed by other users.
    @commands.command(help='Sends a predefined link')
    async def link(self,ctx):
        await ctx.send('https://li.nk/abcdefghijkl')

async def setup(bot): 
    await bot.add_cog(basic_commands(bot))
