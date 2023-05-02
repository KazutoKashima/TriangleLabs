import discord
from discord import app_commands
from discord.ext import commands
from bot_revision import client

class General(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="help", description="Shows the help menu")
    async def help(self, ctx: discord.Interaction) -> None:
        await ctx.response.send_message(f"**List of commands available for {client.user.mention}:**\n\n - {client.user.mention} activate -- to enable shape to talk in channel.\n - {Client.user.mention} deactivate -- to stop shape from talking in channel\n - {Client.user.mention} wack -- reset conversation history of the bot to yourself\n\n**notes**:\n - first 2 can only be run by admins.\n - pls make sure to give {Client.user.mention} send message and read channel perms.\n - you can also DM {Client.user.mention} to chat.\n - if u have any issues or want to make ur own shape like {client.user.mention}, join our guild https://discord.gg/qxwTY2x5N7", ephemeral=True)
    
    @app_commands.command(name="ping", description="Shows the latency of the bot")
    async def ping(self, ctx: discord.Interaction) -> None:
        await ctx.response.send_message(f"Pong! {round(client.latency * 1000)}ms", ephemeral=True)
        
    @app_commands.command(name="support", description="Shows the support server")
    async def support(self, ctx: discord.Interaction):
        await ctx.response.send_message("Support for this bot can be found at https://discord.gg/qxwTY2x5N7", ephemeral=True)
	
async def setup(client: commands.Bot):
    client.add_cog(General(client))