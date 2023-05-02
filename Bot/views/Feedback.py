from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle
from bot_revision import Moderation, base_dir
from datetime import datetime

class Feedback_Form(Modal, title="TriangleLabs Feedback Form"):
	feedback = TextInput(
		label="Type Your feedback below (min 100 characters)",
		placeholder="Write some detailed feedback here...",
		style=TextStyle.long, min_length=100
	)

	async def on_submit(self, ctx: Interaction):
		if Moderation.Not_Banned_User(id=ctx.user.id):
			await ctx.response.send_message("Your feedback has been submitted.")
			# Write feedback to a per user file
			with open(f"{base_dir}/feedback/{ctx.user.id}", "a+") as f:
				time = datetime.now()
				# convert time to DD-MM-YYYY HH:MM:SS
				converted_time = time.strftime("%d-%m-%Y %H:%M:%S")
				f.write(f"{converted_time} - {ctx.user.name}: \n{self.feedback}\n\n")
				f.close()
		else:
			await ctx.response.send_message("You are banned from using this bot.", ephemeral=True)
   