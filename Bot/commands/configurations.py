import discord
from discord import app_commands
from discord.ext import commands
from bot_revision import client, base_dir
from trianglelabs import Discord

class AIConfigs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="activate", description="Enables the bot to talk in the channel")
    async def activate(self, ctx: discord.Interaction) -> None:
        if Discord.is_dm_channel(ctx) or ctx.user.guild_permissions.administrator:
            os.system(f"touch {base_dir}/clients/{ctx.client.user.id}/channels/{ctx.channel_id}")
            await ctx.response.send_message(
                content=await Discord.parse_message(f"{ctx.client.user.name} has been enabled")
            )
        else:
            await ctx.response.send_message("Missing Permissions.")
    
    @app_commands.command(name="deactivate", description="Disables the bot to talk in the channel")
    @commands.has_permissions(administrator=True)
    async def deactivate(self, ctx: discord.Interaction) -> None:
        if ctx.author.guild_permissions.administrator == True:
            os.system(f"rm {base_dir}/clients/{ctx.client.user.id}/channels/{ctx.channel_id}")
            await ctx.response.send_message(
				content=await Discord.parse_message(f"{ctx.client.user.name} has been disabled")
			)
        else:
            await ctx.response.send_message("Missing Permissions.")

async def setup(client: commands.Bot):
    client.add_cog(AIConfigs(client))
