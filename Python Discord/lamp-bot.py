# bot.py
# Pre-Requits:
# pip install -U discord.py
# pip install -U python-dotenv
import os
import random

import discord
from discord import message
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Q!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    happy_birthday_message = [
        'Happy Birthday!!! 🎉',
        'Count your life by smiles, not tears. Count your age by friends, not years. Happy birthday!',
        (
            'Another adventure filled year awaits you.' 
            'Welcome it by celebrating your birthday with pomp and splendor.'
            'Wishing you a very happy and fun-filled birthday!'
        ),
        'Happy birthday! I hope all your birthday wishes and dreams come true.',
    ]

    if message.content == 'happy birthday':
        response = random.choice(happy_birthday_message)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    #await message.channel.send('Oh I found error! 😢 \nI think you ought to know I’m feeling very depressed.')
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)