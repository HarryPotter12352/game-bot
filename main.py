import configparser
import discord
from discord.ext import commands
from utils.create_db import create_prefix_db


bot = commands.Bot(command_prefix="./", owner_ids={737540230957105254, 852788943229288449})
bot.db = bot.loop.run_until_complete(create_prefix_db())
bot.load_extension("jishaku")


config = configparser.ConfigParser()
config.read("config.ini")


@bot.event
async def on_ready():
    print(f"{bot.user} is now ready!")


bot.run(config["credentials"]["token"])
