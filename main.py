from typing import Optional
import discord  # discord.py module
import random
import time
import aiohttp
import asyncio
import decimal
from discord.ext import commands

prefix = "-"


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-help"))

    async def on_message(self, message):
        channel = message.channel.name
        restricted_channels = ["chat", "chung", "nối từ"]  # List of restricted channels
        if message.author.bot:
            return
        if message.content.startswith(prefix):
            command = message.content[len(prefix):]  # Get the command
            emoji_1 = '✅'
            emoji = discord.utils.get(client.emojis, name='moe')
            channel_polls_id = client.get_guild(882259911650713670).get_channel(1036084278037053474)
            eightball_ans = ['Yes', 'Absolutely Yes', 'No', 'Never',
                             'Maybe', 'I dont know']
            unsplash = 'Z2ryujB4A9QW5Wf68n3tm_66o89gCFZ2C-mAytlMrHw'
            client.ses = aiohttp.ClientSession()
            if command == "hello":
                await message.channel.send(f"Hello {message.author.mention}!I'm namg125's bot.{str(emoji)}")

            if command == "help":
                await message.add_reaction(emoji_1)
                await message.reply("```\n"
                                    "Commands:\n"
                                    "prefix : -\n"
                                    "google: 'text'- Help you search text in google\n"
                                    "spotify: 'text'- Help you search text song in spotify\n"
                                    "8ball: 'text- Answer your question.Only Yes/No type question\n"
                                    "rip: 'text' - Create a rip stone with word\n"
                                    "rdimage: 'text' - This command random image with 1 word\n"
                                    "avatar: - To see your avatar\n"
                                    "delete: 'number' - Delete user's number prompt\n"
                                    "poll: 'text' - first text is question(s) next text is option(s), you split by';'\n"
                                    "-------------------------------------------------\n"
                                    "❗POLL STILL ON DEVELOP, WE WILL FIX IT SOON❗\n"
                                    "💠There will be some update in the future💠\n"
                                    "```")
            if command.startswith('google:'):
                gg = command.split(": ", 2)[1:]
                await message.reply(f"https://www.google.com/search?q={(gg[0])}")
            if command.startswith('spotify:'):
                spo = command.split(": ", 2)[1:]
                await message.reply(f"https://open.spotify.com/search/{(spo[0])}")
            if command.startswith('8ball:'):
                await message.reply(random.choices(list(eightball_ans)))
            if command.startswith('rip: '):
                rip_stone = command.split(": ", 2)[1:]
                await message.reply(f"http://www.tombstonebuilder.com/generate.php?top1={(rip_stone[0])}")
            if command.startswith('rdimage'):
                image_r = command.split(" ", 1)[1:]
                url = f"https://source.unsplash.com/featured/?{(image_r[0])}"
                async with client.ses.get(url) as r:
                    if r.status in range(200, 299):
                        mbed_r = discord.Embed(
                            title='Here is your image', color=discord.Color.random()
                        ).set_image(url=url)
                        await message.reply(embed=mbed_r)
            if command.startswith('avatar'):
                profile = message.author
                await message.reply(profile.avatar.url)
            if command.startswith('delete'):
                delete_num = int(command.split(" ", 1)[1])
                if delete_num < 0:
                    await message.reply("Please enter a positive integer.")
                    return
                if delete_num > 100:
                    await message.reply("You can only delete up to 100 messages at a time.")
                    return
                with message.channel.typing():
                    deleted = await message.channel.purge(limit=delete_num + 1)
                await message.channel.send(f"Deleted {len(deleted) - 1} messages.", delete_after=5)
            if command.startswith('polls'):
                p_polls = command.split(" ; ", 3)[1:]
                if len(p_polls) >= 2:
                    options_p = p_polls[1]
                    options_polls = options_p.split(" ", 10)[0:]
                    questions_p = p_polls[0]
                    if len(options_polls) <= 1:
                        await message.send("You need to provide at least 2 options.")
                        return
                    if len(options_polls) > 10:
                        await message.send("You can't provide more than 10 options.")
                        return

                    # create the poll message
                    message_polls = f"**{questions_p}**\n"
                    for i, option in enumerate(options_polls):
                        message_polls += f"{i + 1}\U000020e3 {option}\n"

                    poll = await channel_polls_id.send(message_polls)
                    # add reactions to the poll message
                    for i in range(len(options_polls)):
                        emojis = f"{i + 1}\U000020e3"
                        await poll.add_reaction(emojis)
                    # countdown timer
                    duration_p = 10  # set the duration to 60 seconds (change as needed)
                    for i in range(duration_p):
                        await asyncio.sleep(1)
                        time_left = duration_p - i
                        if time_left % 10 == 0:
                            await poll.edit(content=f"{message_polls}\n\n**Time Left:** {time_left} seconds")

                    # get poll results
                    poll = await channel_polls_id.fetch_message(poll.id)
                    reactions = poll.reactions
                    results = []
                    voters = 0
                    for reaction in reactions:
                        for ind, emoji in enumerate(emojis):
                            if reaction.emoji == emoji:
                                results[ind + 1] = reaction.count - 1
                                if reaction.count > 1:
                                    voters += 1

                    # create results message
                    message_results = ""
                    for ind, count in enumerate(results):
                        percent_p = round(results[ind + 1] / voters * 100)
                        message_results += f"{options_polls[ind]} ~ {percent_p}% ({results[ind + 1]} votes)\n"
                    # send poll message with results
                    embed = discord.Embed(title=f"POLL RESULTS: {questions_p}", description=results,
                                          color=discord.Color.random())
                    await channel_polls_id.send(embed=embed)
                    #delete old poll message
                    await poll.delete()

        if channel in restricted_channels:
            delete_in_restrict = 1
            await message.add_reaction('❌')
            await message.channel.purge(limit=delete_in_restrict + 1)
            await asyncio.sleep(0.5)
            await message.channel.send(f"{message.author.mention}You can't use commands in "
                                       f"{message.channel.mention}", delete_after=1.5)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(BOT_TOKEN)
