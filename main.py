import discord
from discord.ext import commands
from config import config


client = commands.Bot(command_prefix="./")



@client.event 
async def on_ready():
    print(f'{client.user} is now ready!')


client.run(config.get_token())