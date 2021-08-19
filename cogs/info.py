import discord
from discord.ext import commands
from typing import Mapping, Optional
from difflib import get_close_matches as match


class Help(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        ctx = self.context

        embed = discord.Embed(title=f"Hey there {ctx.author.name}", color=ctx.author.color)

        for cog, cmds in mapping.items():
            command_signatures = [self.get_command_signature(c) for c in cmds]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                if cog_name not in ["dev", "jishaku"]:
                    embed.add_field(name=cog_name, value=", ".join([f'`{c.name}`' for c in cmds]), inline=False)

        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        ctx = self.context

        embed = discord.Embed(title=command.name, description='<> - required\n[] - optional', color=ctx.author.color)

        embed.add_field(name="Category", value=command.cog_name, inline=False)
        embed.add_field(name="Help", value=command.help, inline=False)

        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        embed.add_field(name="Usage", value=f'`{ctx.clean_prefix}{command.name} {command.signature}`', inline=False)

        if hasattr(command._buckets._cooldown, "per"):
            embed.add_field(name="Cooldown", value=f"{command._buckets._cooldown.per}s")

        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_group_help(self, group):
        ctx = self.context

        embed = discord.Embed(title=group.qualified_name, color=ctx.author.color)
        embed.add_field(name="Category", value=group.cog_name)
        embed.add_field(name="Description", value=group.short_doc, inline=False)

        desc = "None"
        commands = group.commands
        if len(commands) != 0:
            desc = ", ".join([f'`{c.name}`' for c in commands])

        embed.add_field(name="Commands", value=desc, inline=False)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_cog_help(self, cog):
        ctx = self.context

        embed = discord.Embed(title=cog.qualified_name, color=ctx.author.color)
        embed.add_field(name="Description", value=cog.description, inline=False)

        desc = "None"
        commands = cog.get_commands()
        if len(commands) != 0:
            desc = ", ".join([f'`{c.name}`' for c in commands])

        embed.add_field(name="Commands", value=desc)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    def command_not_found(self, command):
        out = f"Command `{command}` not found"
        matches = match(command, list(self.context.bot.all_commands), n=1)
        if matches:
            out += f". Did you mean `{matches[0]}`?"
        return out
    
    def subcommand_not_found(self, command, subcommand):
        out = f"Subcommand `{subcommand}` of command `{command.name}` not found"
        matches = match(subcommand, [c.name for c in command.commands], n=1)
        if matches:
            out += f". Did you mean `{matches[0]}`?"
        return out


class Info(commands.Cog):
    """information related commands"""

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

        self.bot.help_command: Help = Help(
            command_attrs={"aliases": ["commands", "h"]}
        )
        self.bot.help_command.cog = self

def setup(bot):
    bot.add_cog(Info(bot))