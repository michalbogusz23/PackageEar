from flask import Flask, render_template, request, make_response, session, redirect, url_for
from flask_session import Session
from os import getenv
from dotenv import load_dotenv
from datetime import datetime
import sys # for debugging
from bcrypt import hashpw, gensalt, checkpw

from redis import Redis
db = Redis(host='redis', port=6379, db=0)

load_dotenv()

SESSION_TYPE="redis"
SESSION_REDIS=db
# SESSION_COOKIE_SECURE = True
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = getenv('SECRET_KEY')
ses = Session(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sender/register', methods=['GET'])
def register_form():
    return render_template("register_form.html")

@app.route('/sender/register', methods=['POST'])
def register():
    empty_fields_counter = 0
    user = {}
    data = request.form
    fields = ("firstname", "lastname", "login", "email", "password", "passwordCheck", "address")
    for field in fields:
        if data[field] == '':
            empty_fields_counter += 1
        else:
            user[field] = data[field]
    
    if empty_fields_counter != 0:
        return redirect(url_for("register_form"))

    save_user(user)
    return redirect(url_for("login_form"))

@app.route('/sender/login', methods=['GET'])
def login_form():
    if "user" in session:
        return redirect(url_for("user"))
    return render_template("login_form.html")

@app.route('/sender/login', methods=['POST'])
def login():
    login = request.form["login"]
    password = request.form["password"]
    if verify_user(login, password):
        session["user"] = login
        session["login_date"] = datetime.now()
        return redirect(url_for("user"))
    return redirect(url_for("login"))

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else: 
        return redirect(url_for("login"))

@app.route("/sender/logout")
def sender_logout():
    session.clear()
    login = None
    return redirect(url_for("index"))


def save_user(user):
    salt = gensalt(5)
    password = user['password'].encode()
    hashed = hashpw(password, salt)
    user['password'] = hashed

    login = user['login']
    del user['login']

    db.hmset(f"user:{login}", user)

    return True

def verify_user(login, password):
    password = password.encode()
    hashed = db.hget(f'user:{login}', "password")
    if not hashed:
        print(f"ERROR: No password for {login}", file=sys.stderr)
        return False

    return checkpw(password, hashed)

def is_user(login):
    return db.hexists(f"user:{login}", "password")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)