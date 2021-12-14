from flask import Flask, render_template
import psycopg2 

def query_db():
    conn = psycopg2.connect(
                      host='yourhost',
                      database='yourdb',
                      user='youruser',
                      password='yourpassword')
    
    cursor = conn.cursor()

    query1 = """SELECT * FROM "Content" ORDER BY content_id DESC LIMIT 100;"""

    cursor.execute(query1)

    results1 = cursor.fetchall()

    cursor.close()
    conn.close()

    return results1

def format_result(result):
    text = ""

    for x in range(100):
        channel = result[x][1]
        username = result[x][2]
        message = result[x][3]
        line = "({}) {}: {}".format(channel, username, message)
        text += '<p>{}</p>'.format(line)
    
    return text


app = Flask(__name__)

@app.route("/") #http://localhost:5000/
def front():
    info = query_db()
    content = format_result(info)

    return content

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/back')
def back():
    return '<h1>You\'re at the back page!</h1>'
