import random
import time

from twitchio.ext import commands
from twitchio.client import Client

import credentials

import pyodbc 



CHANNEL = credentials.CHANNEL
NAME = credentials.NAME
TWITCH_TOKEN = credentials.TWITCH_TOKEN
TWITCH_CLIENT_ID = credentials.TWITCH_CLIENT_ID
TWITCH_CLIENT_SECRET = credentials.TWITCH_CLIENT_SECRET

bot = commands.Bot(
    irc_token=TWITCH_TOKEN,
    client_id=TWITCH_CLIENT_ID,
    nick=NAME,
    prefix='!',
    initial_channels=CHANNEL,
)


client = Client(
    client_id=TWITCH_CLIENT_ID,
    client_secret=TWITCH_CLIENT_SECRET,
)

def insert(user, channel, content):
    query = """
            INSERT INTO Content (username, channel, message) VALUES (?, ?, ?)
            """
    
    cursor.execute(query, user, channel, content)

# Actual listener which stores what it hears to a txt file
@bot.event
async def event_message(ctx):
    name = str(ctx.author.name)
    channel = str(ctx.author.channel)
    content = str(ctx.content)
    
    print(name)
    print(content)

    insert(name, channel, content)
    
    await bot.handle_commands(ctx)



if __name__ == '__main__':
    
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=YOURSERVER;'
                      'Database=YOURDATABASE;'
                      'Trusted_Connection=yes;', autocommit=True)

    cursor = conn.cursor()

    bot.run()
