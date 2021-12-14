# TwitchListener
Listens in on Twitch chats and stores data into SQL Table. 

# Install/Setup

1. Make sure you have python 3+ installed.
2. Download the files in this repo and put them in a folder together.
3. In a terminal type ``pip install -r requirements.txt`` while in the folder directory.
4. Set up your user credentials in credentials.py. **NOTE: Do Not Share These Credentials With Anyone!**
5. Create your database/tables such as in table_creation.sql
6. In the terminal type `python TwitchListener.py`
7. You're done!

# FAQ

> How does it work? 

With a twitch account set up you can get the information for credentials.py. Once that is set up, running the program essentially makes the account set up read the twitch chat of any channel you've set in your channels list. Each time a message occurs, it gets inserted into your database. You technically only need one table set up, such as a content table storing the username, channel (as in, what channel was the message on), and message. Optionally you can (and shoulder) include content_id and set up other tables to track users and channels. 

> Can I use this with SQL Server/Ingres/Oracle/etc?

This program uses PostgreSQL. If you wish to use a different database you'll likely need pyodbc instead of psycopg2. The the way it works is very similar and you can find in this repository the original TwitchListener.py which used pyodbc + SQL Server. 

> Backups?

You can create backups with [pg_dump](https://www.postgresql.org/docs/9.1/backup-dump.html). With pydrive you can move your backups to a Google Drive. A simple backup python script is given as backupdb.py. You may need to add your user to postgres to run it without elevated permissions.

# To Do

1. ~~Collect twitch content and insert into database~~
2. ~~Create automatic backup schedule to cloud storage~~
3. Display data on web
