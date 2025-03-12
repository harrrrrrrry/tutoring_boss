from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

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
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    return render_template('menu.html')


@app.route('/login', methods=['POST', 'GET'])
def render_login_page():
    return render_template('login.html')
@app.route('/signup', methods=['POST', 'GET'])
def render_signup_page():
    if request.method == "post":
        fname = request.form.get("user_fname")
    return render_template('signup.html')


app.run(host='0.0.0.0', debug=True)
