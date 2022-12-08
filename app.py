from flask import Flask, render_template, request, redirect, session, flash
import pymysql
import secrets

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret
db = pymysql.connect(user="root", database='nusantamart')


@app.route('/')
def index():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login():
    cursor = db.cursor()
    nama = request.form['nama']
    email = request.form['email']
    password = request.form['password']
    query = "SELECT * FROM `users` WHERE email = %s"
    cursor.execute(query, (email))
    data = cursor.fetchall()
    if (len(data) > 0):
        return index()

    query = "INSERT INTO `users`(`id`,`nama`,`email`,`password`) VALUES(null,%s,%s,%s)"

    cursor.execute(query, (nama, email, password))
    db.commit()

    query = "SELECT `id` FROM `users` WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    data = cursor.fetchall()
    session['user_id'] = data[0]

    return redirect('/homepage')


@app.route('/homepage')
def homepage():
    return render_template('homepage.html', id=session['user_id'])


@app.route('/profile')
def profile():
    query = "SELECT * FROM `users` WHERE id=%s"
    cursor = db.cursor()
    cursor.execute(query, (session['user_id']))
    data = cursor.fetchone()
    return render_template('profile.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
