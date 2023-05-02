# Default/Basic Imports
import os, sys, time, random, asyncio
import discord
from io import StringIO
from typing import List
from discord.ext import commands, tasks

# Include our files
from trianglelabs import Discord, Moderation, AI, langdetect, langcodes, translators, asyncify
import trianglelabs

# Set the current Working Directory to this directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Set our global vars
version = "0.2.1"
base_dir = f"{trianglelabs.config['DATABASE']}"

client = Discord.create_client()

@client.event
async def on_ready():
    try:
        del trianglelabs.config["token"]
    except:
        pass
    
    await Discord.parse_presence(
        Client=Client,
        activitytype=trianglelabs.config["activity"],
        status=trianglelabs.config["status"],
        stream_link=trianglelabs.config["stream_link"]
    )
    
    folders = ['user_info/likes', 'user_info/dislikes', 'user_info/language', 'user_info/roleplay', 'user_info/limits', 'clients', 'images', 'feedback']
    clientFolders = ['users', 'channels', 'story_mode', 'engine', 'message_context']
    if not os.path.exists(base_dir):
        os.system("command mkdir %s" % base_dir)
    for folder in folders:
        if not os.path.exists(f"{base_dir}/{folder}"):
            os.system("mkdir %s" % f"{base_dir}/{folder}")
    if not os.path.exists(f"{base_dir}/clients/{Client.user.id}"):
        os.system("mkdir %s" % f"{base_dir}/clients/{Client.user.id}")
    for folder in clientFolders:
        if not os.path.exists(f"{base_dir}/clients/{Client.user.id}/{folder}"):
            os.system("mkdir %s" % f"{base_dir}/clients/{Client.user.id}/{folder}")

    await Client.tree.sync()
    
for cmd in os.listdir("./commands"):
    if cmd.endswith(".py"):
        client.load_extension(f"cogs.{cmd[:-3]}")

@client.event
async def on_message(message):
    if not Discord.sent_by_bot(message) and Moderation.Not_Banned_User(message.author.id):
        if Discord.is_command(message):
            await Client.process_commands(message)
        else:
            if Discord.is_dm_channel(message) or os.path.exists(f"{base_dir}/clients/{Client.user.id}/channels/{message.channel.id}"):
                # Fetch CTX for typing status and read channel history
                try:
                    try:
                        user_activites = ""
                        for activity in message.author.activities:
                            if isinstance(activity, Spotify):
                                user_activites += "\nYour Friend is currently listening to the song %s by %s" % (activity.title, activity.artist)
                            else:
                                user_activites += "\nYour Friend is playing %s" % activity.name
                    except:
                        user_activites = ""
                    ctx = await Client.get_context(message)
                    if message.reference is not None:
                        original_message = await ctx.fetch_message(message.reference.message_id)
                    if message.reference is None or original_message.author.id == Client.user.id or Client.user.mention in message.content or Client.user.name in message.content:
                        if (message.content[:2] == "<@" and str(Client.user.id) not in message.content) or (Client.user.name not in message.content) or (ctx.guild.get_member(vars.Client.user.id).display_name not in message.content):
                            if not trianglelabs.Limits.is_limited(message):
                                async with ctx.typing():
                                    if os.path.exists(f"{base_dir}/clients/{Client.user.id}/engine/{ctx.channel.id}"):
                                        with open(f"{base_dir}/clients/{Client.user.id}/engine/{ctx.channel.id}") as conf:engine = int(conf.read().replace("\n", "")); conf.close()
                                    if engine not in [3, 4]:
                                        data = await AI.Response.wrap_content(message, ctx, user_activity=user_activites)
                                    elif engine == 4:
                                        data = await AI.Response.wrap_content_gpt(message, ctx, 0, user_activity=user_activites)
                                    else:
                                        data = await AI.Response.wrap_content_gpt(message, ctx, 0, user_activity=user_activites)
                                    if isinstance(data, str):
                                        is_not_safe = await asyncify(Discord.is_safe_message, data)
                                    else:
                                        __data = ""
                                        for i in data:
                                            __data += f'{i["role"]}: {[i["content"]]}'
                                        is_not_safe = await asyncify(Discord.is_safe_message, __data)
                                    message_is_unsafe = await asyncify(Discord.is_safe_message, message.content)
                                    if not (is_not_safe and message_is_unsafe):
                                        file = f"{base_dir}/clients/{Client.user.id}/users/{message.author.id}"
                                        os.system(f"echo {message.id} >> {file}")
                                        __msg_content = await AI.Response.prompt(data, 1, ctx)
                                        try:
                                            language_store = base_dir + "/user_info/language/" + str(message.author.id)
                                            if os.path.exists(language_store):
                                                with open(language_store) as language:
                                                    __original_language = language.read().replace("\n", "")
                                                    language.close()
                                            else:
                                                __original_language = langcodes.standardize_tag("en")
                                            loop=asyncio.get_event_loop()
                                            msg2 = await asyncio.to_thread(translators.translate_text, query_text=__msg_content, to_language=__original_language)

                                            __msg_content = msg2
                                        except:...
                                        if __msg_content.count("```") == 2:
                                            __msg_content = __msg_content.split("```")
                                            code = __msg_content[1]
                                            __msg_content[0] = __msg_content[0].replace(":", ".")
                                            __msg_content.pop(1)
                                            __msg_content[1] = __msg_content[1].replace(":", ".")
                                            __msg_content = ' '.join(__msg_content)
                                            embed = discord.Embed(description=f"```{code}```")
                                            __new_msg_content = []
                                            for i in __msg_content.split("\n"):
                                                if i not in ["\n", "", " "]:
                                                    __new_msg_content.append(i)
                                            __new_msg_content = '\n'.join(__new_msg_content)
                                            __msg_content = __new_msg_content
                                            await Discord.reply(message, __msg_content, 1, embed=discord.Embed(title="Generated Code", description=f"```{code}```"))
                                        else:
                                            await Discord.reply(message, __msg_content, 1)
                                    else:
                                        await message.add_reaction("❌")
                            else:
                                await Discord.reply(message, "You have reached the maximum amount of messages for the day", 0)
                except openai.error.RateLimitError:
                    await Discord.reply(message, "Unfortunately, we are out of funding for the month :(\nPlease support us at https://www.patreon.com/trianglelabs :hearts:", 1)

try:
    Client.run(trianglelabs.config["token"].replace("\n", ""))
except discord.errors.LoginFailure:
    bots_store = base_dir + "/client_launchers/" + trianglelabs.config["__num"] + "/DONOTTOUCH"
    os.system("touch %s" % bots_store)
    print("Failed to log in")
except discord.errors.PrivilegedIntentsRequired:
    bots_store = base_dir + "/client_launchers/" + trianglelabs.config["__num"] + "/DONOTTOUCH2"
    os.system("touch %s" % bots_store)
    print("Missing Intents")