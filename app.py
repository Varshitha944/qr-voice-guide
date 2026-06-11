from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS instructions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT,
        content TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM instructions")
    instructions = cur.fetchall()

    conn.close()

    return render_template('index.html',
                           instructions=instructions)

@app.route('/speak/<language>')
def speak(language):

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT content FROM instructions WHERE language=?",
        (language,)
    )

    result = cur.fetchone()

    cur.execute(
        "INSERT INTO scans(language) VALUES(?)",
        (language,)
    )

    conn.commit()
    conn.close()

    return result[0]

@app.route('/admin')
def admin():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM instructions")
    data = cur.fetchall()

    conn.close()

    return render_template('admin.html', data=data)

@app.route('/add', methods=['POST'])
def add():

    language = request.form['language']
    content = request.form['content']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO instructions(language,content) VALUES(?,?)",
        (language, content)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)