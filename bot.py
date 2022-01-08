# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from weightCheck import weighting

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='weight', help='Returns the weight of a gem')
async def weight(weight, *args):
    if not args:
        response = "fuck you"
    else:
        response = weighting(str(args[0]))
    await weight.send(response)
bot.run(TOKEN)