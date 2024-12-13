import os

import discord
from discord.ext import commands
import re  # Import the regex module

# Create a dictionary to store messages per user
user_messages = {}

# Define bot and its command prefix
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: On bot ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Event: On message
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    specific_channel_id = 1315794669069664317  # Replace with your channel ID
    if message.channel.id == specific_channel_id:
        date_pattern = r"^\d{2}\.\d{2}\.\d{4}\.$"
        if not re.match(date_pattern, message.content):
            try:
                await message.delete()
                await message.channel.send(
                    "Please use the `DD.MM.YYYY.` format. If the digit slot is empty, use 0 (e.g., 03.08.2024).",
                    delete_after=10
                )
            except discord.Forbidden:
                print("Bot lacks permissions to delete messages.")
        else:
            if message.author.id not in user_messages:
                user_messages[message.author.id] = []
            user_messages[message.author.id].append(message.content)

    await bot.process_commands(message)

# Command: View messages
@bot.command(name="history")
async def my_messages(ctx):
    user_id = ctx.author.id
    messages = user_messages.get(user_id, [])
    if messages:
        messages_str = "\n".join(messages)
        await ctx.author.send(f"This is your streak log:\n{messages_str}")
    else:
        await ctx.author.send("You have no messages recorded in this channel.")

# Get the token from environment variables
bot.run(os.getenv("DISCORD_BOT_TOKEN"))