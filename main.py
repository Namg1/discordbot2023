import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents, activity=discord.Game(name="-help"))
bot.remove_command("help")
uploaded_images = []

@bot.command()
async def upload(ctx):
    if len(ctx.message.attachments) > 0:
        for attachment in ctx.message.attachments:
            uploaded_images.append(attachment.url)
        await ctx.send("Images uploaded successfully.")
    else:
        await ctx.send("No images attached.")

@bot.command()
async def send(ctx):
    channel = ctx.channel
    if uploaded_images:
        image_url = random.choice(uploaded_images)
        await channel.send(image_url)
    else:
        await ctx.send("No images uploaded yet.")

@bot.command()
async def clear(ctx):
    uploaded_images.clear()
    await ctx.send("Uploaded images cleared.")

bot.run("token")
