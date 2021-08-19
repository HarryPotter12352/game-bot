import configparser
import discord
from discord.ext import commands
from utils import create_prefix_db

async def get_prefix(bot, message):
    async with bot.db.cursor() as c:
        await c.execute("SELECT prefix FROM prefix_data WHERE guild_id = ?", (message.guild.id,))
        data = await c.fetchone()
        return data[0]


bot = commands.Bot(command_prefix=get_prefix, owner_ids={737540230957105254, 852788943229288449})
bot.db = bot.loop.run_until_complete(create_prefix_db())

bot.load_extension("jishaku")
for cog in ("info",):
    bot.load_extension(f"cogs.{cog}")


config = configparser.ConfigParser()
config.read("config.ini")


@bot.event
async def on_ready():
    print(f"{bot.user} is now ready!")

@bot.event
async def on_guild_join(guild):
    async with bot.db.cursor() as c:
        await c.execute("INSERT INTO prefix_data VALUES (?, ?)", (guild.id, "./"))
        await bot.db.commit()

@bot.event
async def on_guild_remove(guild):
    async with bot.db.cursor() as c:
        await c.execute("DELETE FROM prefix_data WHERE guild_id = ?", (guild.id,))
        await bot.db.commit()

@bot.command()
async def prefix(ctx, new_prefix = None):
    old_prefix = ctx.prefix
    if new_prefix:
        async with bot.db.cursor() as c:
            await c.execute("UPDATE prefix_data SET prefix = ? WHERE guild_id = ?", (new_prefix, ctx.guild.id))
            await bot.db.commit()
        await ctx.send(f"Changed prefix from `{old_prefix}` to `{new_prefix}`")

    if not new_prefix:
        return await ctx.send(f"My prefix for this server is `{old_prefix}`!")


bot.run(config["credentials"]["token"])
