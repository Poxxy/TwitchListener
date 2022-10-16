from twitchio.ext import commands
import psycopg2 
from dotenv import load_dotenv
import os

load_dotenv()

# credentials
bot_token = os.getenv('bot_token')
db_host = os.getenv('db_host')
db_database = os.getenv('db_database')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')

#channels to join
bot_channels = ['waltzingstoic']


class Bot(commands.Bot):

    

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=bot_token, prefix='?', initial_channels=bot_channels)

        #Add users here who has permission to issue commands
        self.COMMANDERS = [self.nick, 'waltzingstoic']
    
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
        
        name = str(message.author.name)
        channel = str(message.author.channel)
        content = str(message.content)
        timestamp = str(message.timestamp)

        
        cursor.execute("""INSERT INTO "content" (username, channel, message, time) VALUES (%s, %s, %s, %s)""", (name, channel, content, timestamp))
        conn.commit()
        

        # Print the contents of our message to console...
        #print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        if ctx.author.name in self.COMMANDERS:
            await ctx.send(f'Hello {ctx.author.name}!')


conn = psycopg2.connect(
                      host=db_host,
                      database=db_database,
                      user=db_user,
                      password=db_pass)

cursor = conn.cursor()

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.

#Good practice to close out when done!
cursor.close()
conn.close()
