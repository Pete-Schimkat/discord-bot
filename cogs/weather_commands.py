from typing import ValuesView
from discord.ext import commands 
import discord
from discord.ext.commands.bot import Bot
import asyncio
import aiohttp
import os
import datetime

#TODO: Look into this shit, https://www.tomorrow.io/blog/creating-daily-forecasts-with-a-python-weather-api/
#TODO: Bad Aiblingen
#TODO: Berliner Bezirke

tomorrow_io_key = os.getenv('WEATHER_API')

url = 'https://api.tomorrow.io/v4/timelines'
schlosspark_coordinates = [52.576184, 13.409097]
timezone = "Europe/Berlin"

pankow_query = {
"location":"52.576184, 13.409097",
"fields":["temperature", "cloudCover",'precipitationProbability','temperatureApparent','weatherCode'],
"units":"metric",
"timesteps":"current",
"timezone":"Europe/Berlin",
"apikey":tomorrow_io_key}

class weather_commands(commands.Cog,name='weather'):
    def __init__(self,bot):
        self.bot = bot
        self.description='Check weather data for any location'

    @commands.command(help="Shows current weather in pankow")
    async def pankow(self,ctx):
        async with self.bot.session.get(url,params=pankow_query) as resp: 
            result = (await resp.json())['data']['timelines'][0]['intervals'][0]['values']
            t = result['temperature']
            tt =result['temperatureApparent']
            c = result['cloudCover']
            r = result['precipitationProbability']
            code = result['weatherCode']
            await ctx.send(f"Currently {str(round(t))}°C in Pankow - Perceived: {round(tt)}°C | Clouds: {str(c)}% | Rain: {str(r)}% | Weather: "+str(weatherCode[str(code)]))
                
                

    @commands.command(help="sends a forecast of weather in pankow fore the next couple of days",aliases=["fcberlin"])
    async def forecast_berlin(self,ctx):
        query= {
            "location":"52.516070227858776, 13.401151198369881",
            "units":"metric",
            "timesteps":"1d",
            "fields":["temperature","weatherCode","cloudCover","precipitationProbability"],
            "timezone":"Europe/Berlin",
            "apikey":tomorrow_io_key
        }
        async with self.bot.session.get(url,params=query) as resp:
            sendstring = "Forecast for Berlin:\n"
            results = (await resp.json())['data']['timelines'][0]['intervals']
            for daily_result in results: 
                date = daily_result['startTime'][0:10]
                temp = daily_result['values']['temperature']
                code = daily_result['values']['weatherCode']
                precipitation = daily_result['values']['precipitationProbability']
                date = datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d. %b. %y');
                sendstring = sendstring + f"{date} : Temp.: {str(round(temp))}°C | Rain: {str(precipitation)}% | {str(weatherCode[str(code)])}\n"
            await ctx.send(sendstring)

weatherCode = {
      "0": "Unknown",
      "1000": "Clear, Sunny",
      "1100": "Mostly Clear",
      "1101": "Partly Cloudy",
      "1102": "Mostly Cloudy",
      "1001": "Cloudy",
      "2000": "Fog",
      "2100": "Light Fog",
      "4000": "Drizzle",
      "4001": "Rain",
      "4200": "Light Rain",
      "4201": "Heavy Rain",
      "5000": "Snow",
      "5001": "Flurries",
      "5100": "Light Snow",
      "5101": "Heavy Snow",
      "6000": "Freezing Drizzle",
      "6001": "Freezing Rain",
      "6200": "Light Freezing Rain",
      "6201": "Heavy Freezing Rain",
      "7000": "Ice Pellets",
      "7101": "Heavy Ice Pellets",
      "7102": "Light Ice Pellets",
      "8000": "Thunderstorm"
    }

async def setup(bot): 
    await bot.add_cog(weather_commands(bot))