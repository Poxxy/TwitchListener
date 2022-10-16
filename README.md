# TwitchListener
Listens in on Twitch chats using https://twitchio.dev/en/latest/ and stores data into SQL Table using https://www.postgresql.org/. 

## Example w/ Flask
![Basic Example](https://github.com/Poxxy/TwitchListener/blob/main/example1.png?raw=true)

# Install/Setup

1. Make sure you have python 3+ installed.
2. Download the files in this repo and put them in a folder together.
3. In a terminal type ``pip install -r requirements.txt`` while in the folder directory.
4. Set up your token information in the .env file. **NOTE: Do Not Share These Credentials With Anyone!**
5. Create your database/tables such as in table_creation.sql
6. In the terminal type `python TwitchListener.py`
7. You're done!

# FAQ

> How does it work? 

With a twitch account set up you can get the token information from https://twitchtokengenerator.com/. Once that is set up, running the program essentially makes the account set up read the twitch chat of any channel you've set in your channels list. Each time a message occurs, it gets inserted into your database. You technically only need one table set up, such as a content table storing the username, channel (as in, what channel was the message on), message, and timestamp. Optionally you can (and should) include content_id and set up other tables to track users and channels. 

> Can I use this with SQL Server/Oracle/etc?

This program uses PostgreSQL. If you wish to use a different database you'll likely need pyodbc instead of psycopg2. The the way it works is very similar and you can find in this repository the original TwitchListener.py which used pyodbc + SQL Server. 

> Backups?

You can create backups with [pg_dump](https://www.postgresql.org/docs/9.1/backup-dump.html). With pydrive you can move your backups to a Google Drive. A simple backup python script is given as backupdb.py. You may need to add your user to postgres to run it without elevated permissions.

> Displaying on web?

As an example I use Flask to show messages and other info. You can similarly use your favorite tool to get data from your database and format it for a web page.
