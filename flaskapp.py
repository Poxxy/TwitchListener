from flask import Flask, render_template
import psycopg2 

def query_db(query):
    """
    Executes query. Careful not to open yourself up to SQL injection! 
    You should either only give pre-defined queries or parameterize where input may occur.
    """

    try:
        conn = psycopg2.connect(
                        host='yourhost',
                        database='yourdb',
                        user='youruser',
                        password='yourpassword')
    except psycopg2.OperationalError as e:
        issue = ('Unable to connect!\n{0}').format(e)
        print(issue)
        return issue
    
    cursor = conn.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def format_result(result):
    """
    Makes SELECT query for content table a bit prettier.
    """
    text = ""

    for x in range(100):
        channel = result[x][1]
        username = result[x][2]
        message = result[x][3]
        line = "({}) {}: {}".format(channel, username, message)
        text += '<p>{}</p>'.format(line)
    
    return text

def update_tables():
    users_update_query = """insert into "Users" (username)
    select distinct username
    from "Content"
    where username not in (select username FROM "Users");
    """
    channels_update_query = """insert into "Channels" (channel) 
    select distinct channel 
    from "Content"
    where channel not in (select channel FROM "Channels");
    """

    query_db(users_update_query)
    query_db(channels_update_query)

app = Flask(__name__)

@app.route("/") #http://localhost:5000/
def front():
    query = """SELECT * FROM "Content" ORDER BY content_id DESC LIMIT 100;"""
    info = query_db(query)
    content = format_result(info)

    return content

@app.route("/info")
def info():
    html = """<h1>Information Page</h1>
    """
    user_query = """select * from "Users" ORDER BY user_id DESC;"""

    channel_query = """select * from "Channels" ORDER BY channel_id DESC;"""

    users = query_db(user_query)
    channels = query_db(channel_query)

    return html + "<p>{}</p><p>{}</p>".format(users, channels)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/back')
def back():
    return '<h1>You\'re at the back page!</h1>'
