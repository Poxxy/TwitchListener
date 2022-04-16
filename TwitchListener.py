from twitchio.ext import commands
import psycopg2 

class Bot(commands.Bot):

    

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='YOUR_TOKEN', prefix='?', initial_channels=['YOUR','CHANNELS','HERE'])

        #Add users here who has permission to issue commands
        self.COMMANDERS = [self.nick, 'YOU', 'OTHERS']
    
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
                      host='host',
                      database='db',
                      user='user',
                      password='very_secret')

cursor = conn.cursor()

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.

#Good practice to close out when done!
cursor.close()
conn.close()
