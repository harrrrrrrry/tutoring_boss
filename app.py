from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
DATABASE = "tables_tutoring"

app = Flask(__name__)
def is_logged_in():
    if(session.get('user_id') is None):
        print('not logged in')
        return False
    else:
        print('logged in')
        return True
def connect_database(db_file):
    """
    creates a connection with the database
    :param db_file:
    :return:
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        print(f'an error is here, from database connection place')
    return

@app.route('/')
def render_homepage():
    return render_template('home.html', logged_in=is_logged_in())


@app.route('/menu')
def render_menu_page():
    return render_template('menu.html')


@app.route('/login', methods=['POST', 'GET'])
def render_login():
    if request.method == 'POST':
        email = request.form.get('user_email')
        password = request.form.get('user_password')
        con = connect_database(DATABASE)
        cur = con.cursor()
        query = 'SELECT fristname, last_name, email, password FROM eamil='
        cur.execute(query,(email,))
        results = cur.fetchone()
        print(results)
        if password != results[3]:
            return redirect('/login/message=incorrect+username+or+password')
        session['email'] = results[2]
        session['first_name'] = results[0]
        session['last_name'] = results[1]
        return redirect('/')

    return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def render_signup_page():
    if request.method == "POST":
        fname = request.form.get("user_fname").title().strip()
        lname = request.form.get("user_lname").title().strip()
        email = request.form.get("user_email").lower().strip()
        password = request.form.get("user_password")
        password2 = request.form.get("user_password2")


        if password != password2:
            return redirect("\signup?error=password+do+not+match")

        if len(password) < 8:
            return redirect("\signup?error=passowrd+to+short+,+atleast+8+required")

        if len(password) > 30:
            return redirect("\signup?error=password+is+too+long+,+30+characters+max")
        con = connect_database(DATABASE)
        query_insert = "INSERT INTO user (first_name,last_name, email, password ) VALUES(?,?,?,?)"
        print('flagged thing kaboom')
        cur = con.cursor()
        cur.execute(query_insert,(fname ,lname ,email ,password))
        con.commit()
        con.close()

    return render_template('signup.html')


app.run(host='0.0.0.0', debug=True)
