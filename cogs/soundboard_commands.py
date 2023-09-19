from asyncio.tasks import sleep
from discord.ext import commands
import discord
import os
import random


class soundboard_commands(commands.Cog,name='soundboard'):
    def __init__(self,bot):
        self.bot = bot
        self.description='play pre-defined sounds in a voice channel'

# The following command can be duplicated for as many soundfiles as desired to enable users to directly play multiple sounds in the current voice channel.
# Note that I designed this command before discord implemented their soundboard feature, which makes this cog somewhat obsolete

    @commands.command(help='Plays predefined soundfile in the channel of the user that invoked the command',aliases=["sound"])
    async def soundboardexample(self,ctx):
        await playSound(ctx,'name_of_soundfile')

async def playSound(ctx,name):
        voice_state  = ctx.message.author.voice
        if(voice_state == None): 
            await ctx.send('You need to be in a voice channel to use this command')
        else:
            voice_channel = ctx.message.author.voice.channel
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(f"./audio/{name}.mp3"))
            #vc.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="./okay.mp3"))
            while vc.is_playing():
                await sleep(.1)
            await vc.disconnect()
        await ctx.message.delete()

async def setup(bot): 
    await bot.add_cog(soundboard_commands(bot))
