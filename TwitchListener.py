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
ADMIN = credentials.ADMIN

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

def content_return(user, channel):
    query = """
            SELECT COUNT(Message) FROM Content where username = ? and
            channel = ?
            """.lower()
    cursor.execute(query, user, channel)
    result = cursor.fetchall()[0][0]
    return result

def content_top(channel):
    query = """
            SELECT TOP 3 username, COUNT(*) 
            FROM content
            WHERE channel = ?
            GROUP BY username
            ORDER BY 2 DESC
            """.lower()
    cursor.execute(query, channel)
    result = cursor.fetchall()
    return result


# Actual listener which stores what it hears to a txt file
@bot.event
async def event_message(ctx):
    name = str(ctx.author.name)
    channel = str(ctx.author.channel)
    content = str(ctx.content)

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

# Command to show top 3 highest messengers.
@bot.command(name='mtop')
async def message_top(ctx):
    time.sleep(.5)
    if str(ctx.author.name) in ADMIN:
        channel = str(ctx.author.channel)
        mtop = content_top(channel)
        top1 = mtop[0][0]
        top2 = mtop[1][0]
        top3 = mtop[2][0]
        await ctx.send("Top 3 users in this channel: {}, {}, and {}".format(top1,top2,top3)

# Command to display github page.
@bot.command(name='github')
async def github(ctx):
    time.sleep(.5)
    if str(ctx.author.name) in ADMIN:
        await ctx.send("I'm made by waltzingstoic. You can find my source code on https://github.com/Poxxy/TwitchListener. Thanks!")

if __name__ == '__main__':
    
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=server;'
                      'Database=db;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()

    bot.run()
