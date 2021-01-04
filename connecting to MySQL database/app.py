from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql7384934'
app.config['MYSQL_PASSWORD'] = '1rkpNU3sDZ'
app.config['MYSQL_HOST'] = 'sql7.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql7384934'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
    cur.execute('''INSERT INTO example VALUES (1, 'Ndichu')''')
    cur.execute('''INSERT INTO example VALUES (2, 'Mwangi')''')
    cur.execute('''INSERT INTO example VALUES (3, 'William')''')
    mysql.connection.commit()

    cur.execute('''SELECT * FROM example''')
    results = cur.fetchall()
    print(results)
    return results[0]['name']



if __name__ == '__main__':
    app.run(debug=True)