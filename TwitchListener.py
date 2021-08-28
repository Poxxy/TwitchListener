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

    if 'drop' in query or 'alter' in query:
        print("Query ignored due to possible SQL Injection")
    else:
        cursor.execute(query, user, channel, content)

def content_return(user, channel):
    query = """
            SELECT COUNT(Message) FROM Content where username = ? and
            channel = ?
            """.lower()
    cursor.execute(query, user, channel)
    result = cursor.fetchall()[0][0]
    return result


# Actual listener which stores what it hears to a txt file
@bot.event
async def event_message(ctx):
    name = str(ctx.author.name)
    channel = str(ctx.author.channel)
    content = str(ctx.content)
    
    print(name)
    print(content)

    insert(name, channel, content)
    conn.commit()
    
    await bot.handle_commands(ctx)

# Command which sends back info from database.
@bot.command(name='mcount')
async def message_count(ctx):
    time.sleep(.5)
    user = str(ctx.author.name)
    channel = str(ctx.author.channel)

    mcount = content_return(user, channel)
    await ctx.send("{} you have {} messages in this channel.".format(user, mcount))

# Command to display github page.
@bot.command(name='github')
async def github(ctx):
    time.sleep(.5)
    await ctx.send("You can find my source code on https://github.com/Poxxy/TwitchListener. Thanks!")

if __name__ == '__main__':
    
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=servername;'
                      'Database=dbname;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()

    bot.run()
