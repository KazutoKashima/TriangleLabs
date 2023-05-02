from discord import Interaction, ButtonStyle, Embed, Color
from discord.ui import View, button, Button
from bot_revision import AI
class Enlarge_Image(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    
    @button(label="Enlarge Image", style=ButtonStyle.green, custom_id="enlarge_image", emoji="🔍")
    async def confirm(self, ctx: Interaction, button: Button):
        orignal_image = ctx.message.attachments[0].url
        original_embed = ctx.message.embeds[0]
        await ctx.response.edit_message(embed=Embed(
			title="Enlarging...",
			color=Color.blurple(),
			view=Enlarge_Image_Complete()
		))
        coro = asyncio.to_thread(AI.Upscale.url, orignal_image)
        task = asyncio.create_task(coro)
        url = await task
        embed = original_embed.set_image(url=url).title = "Image Generation Result (Enlarged)"
        await ctx.followup.edit_message(
			embed=embed,
			view=Enlarge_Image_Complete(),
			message_id=ctx.message.id,
		)

class Enlarge_Image_Complete(View):
	def __init__(self):
		super().__init__(timeout=None)
		self.value = None

	@button(label="Enlarge Image", style=ButtonStyle.green, custom_id="enlarge_image", emoji="🔍")
	async def confirm(self, ctx: Interaction, button: Button): ...
  