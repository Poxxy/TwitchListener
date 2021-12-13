import random
import time

from twitchio.ext import commands
from twitchio.client import Client

import credentials

import psycopg2 

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

def insert(user, channel, message):
    
    cursor.execute("""INSERT INTO "Content" (username, channel, message) VALUES (%s, %s, %s)""", (user, channel, message))


# Actual listener which stores what it hears by inserting into the database
@bot.event
async def event_message(ctx):
    name = str(ctx.author.name)
    channel = str(ctx.author.channel)
    content = str(ctx.content)

    insert(name, channel, content)
    conn.commit()
    
    #Enable only if listening for commands.
    #await bot.handle_commands(ctx)


if __name__ == '__main__':
    
    conn = psycopg2.connect(
                      host='your_host',
                      database='your_db',
                      user='your_user',
                      password='your_password')

    cursor = conn.cursor()
    
    bot.run()

    #Good practice to close out when done!
    cursor.close()
    conn.close()
