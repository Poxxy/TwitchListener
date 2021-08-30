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
            """.lower()

    if 'drop' in query or 'alter' in query or 'delete' in query:
        print("Replacing scary words.")
        query = query.replace('drop','dr0p')
        query = query.replace('alter','alt3r')
        query = query.replace('delete','d3l3t3')

    cursor.execute(query, user, channel, content)


# Actual listener which stores what it hears by inserting into the database
@bot.event
async def event_message(ctx):
    name = str(ctx.author.name)
    channel = str(ctx.author.channel)
    content = str(ctx.content)

    insert(name, channel, content)
    conn.commit()
    
    await bot.handle_commands(ctx)


if __name__ == '__main__':
    
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=yourserver;'
                      'Database=yourdb;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()

    bot.run()
