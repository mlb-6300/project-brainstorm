from flask import Flask, render_template, request
from datetime import datetime
import sqlite3 as sql
from cryptography.fernet import Fernet

app = Flask(__name__)

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/adduser', methods = ['POST', 'GET'])
def addUser():
    if request.method == 'POST':
        try:
            user = request.form['Username']
            passwd = f.encrypt(request.form['Password']) 
            dt = datetime.now()
            dob = request.form['DOB']
            gend = request.form['Gender']

            conn = sql.connect('userData.db')
            cur = conn.cursor()

            cur.execute("SELECT Username FROM Users WHERE Username = ?", (user,))
            check = cur.fetchall()

            if not check:
                cur.execute("INSERT INTO Users VALUES(?, ?, ?, ?, ?)", (user, passwd, dt, dob, gend))
                conn.commit()
                conn.close()
            else:
                # need to return error message of some kind. maybe return a render template of some error.html page
                # stating that the username already exists
                print("Username already exists")

        except:
            # need to add stuff here
            pass
     

if __name__ == '__main__':
    app.run('localhost', debug=True)