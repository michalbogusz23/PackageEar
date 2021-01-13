from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from flask_session import Session
from os import getenv
from datetime import datetime
from jwt import encode, decode
from datetime import datetime, timedelta
from time import sleep

import requests
import sys
import db_handler
import json

from redis import StrictRedis

SESSION_TYPE="redis"
SESSION_REDIS=db_handler.db
API_ADDRESS = 'https://secret-island-24073.herokuapp.com/'

NOTIFICATIONS = ['foo', 'bar', 'baz']

# SESSION_COOKIE_SECURE = True
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = getenv('SECRET_KEY')
JWT_SECRET = getenv('JWT_SECRET')
try:
    JWT_EXP = int(getenv('JWT_EXP'))
except ValueError:
    JWT_EXP = 120
except TypeError:
    JWT_EXP = 120

ses = Session(app)

@app.route('/notifications')
def notifications():
    new_notifications = get_notifications()
    while not new_notifications:
        sleep(1)
        print("Checking ... ")
        new_notifications = get_notifications()
    return new_notifications

@app.route('/notify/<msg>')
def notify(msg):
    NOTIFICATIONS.append(msg)
    print("Now the notifications are:")
    print(NOTIFICATIONS)
    return make_response('', 204)

def get_notifications():
    if len(NOTIFICATIONS) > 0:
        return NOTIFICATIONS.pop()
    return None

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
        flash(f"Liczba brakujących pól: {empty_fields_counter}")
        return redirect(url_for("register_form"))
    
    login = data["login"]

    if db_handler.is_user(login):
        flash(f"Użytkownik: {login} już istnieje")
        return redirect(url_for("register_form"))

    if data["password"] != data["passwordCheck"]:
        flash(f"Podane hasła nie są identyczne")
        return redirect(url_for("register_form"))

    user.pop("passwordCheck")

    if db_handler.save_user(user):
        flash(f"Pomyślnie zarejestrowano! Zaloguj się poniżej")
    else:
        return "Database not working", 507
    
    return redirect(url_for("login_form"))

@app.route('/sender/login', methods=['GET'])
def login_form():
    if "user" in session:
        return redirect(url_for("index"))
    return render_template("login_form.html")

@app.route('/sender/login', methods=['POST'])
def login():
    login = request.form["login"]
    password = request.form["password"]

    if not login or not password:
        flash("Brakuje loginu i/lub hasła")
        return redirect(url_for("login_form"))

    if not db_handler.verify_user(login, password):
        flash("Niewłaściwy login i/lub hasło")
        return redirect(url_for("login_form"))

    session["user"] = login
    session["login_date"] = datetime.now()
    return redirect(url_for("index"))

@app.route("/sender/logout")
def sender_logout():
    session.clear()
    login = None
    return redirect(url_for("index"))

def generate_header_with_token():
    username = session["user"]
    payload = {
        'usr': username,
        'type': 'sender',
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP)
    }
    token = encode(payload, JWT_SECRET, algorithm='HS256')
    token = token.decode()
    headers = {"Authorization": "Bearer " + token}
    return headers

@app.route("/sender/dashboard")
def sender_dashboard():
    if "user" not in session:
        flash("Dostęp tylko dla zalogowanych użytkowników!")
        return redirect(url_for("index"))

    headers = generate_header_with_token()
    r = requests.get(API_ADDRESS + 'label', headers=headers)
    if r.status_code != 200:
        return {'error': 'Unauthorized'}, 401

    response = r.json()
    print(response, file=sys.stderr)
    labels = response['labels']
    
    return render_template("packages.html", packages=labels)

@app.route("/package/add", methods=["GET"])
def add_package_form():
    if "user" not in session:
        flash("Dostęp tylko dla zalogowanych użytkowników!")
        return redirect(url_for("index"))

    return render_template("add_package.html")

@app.route("/package/add", methods=["POST"])
def add_package():
    if "user" not in session:
        flash("Dostęp tylko dla zalogowanych użytkowników!")
        return redirect(url_for("index"))

    label = {}
    data = request.form
    fields = ("receiver_name", "box_id", "size")

    if data["size"] not in ["s", "m", "l"]:
        return 'Niewłaściwy rozmiar paczki', 401

    for field in fields:
        label[field] = data[field]

    print(label, file=sys.stderr)
    headers = generate_header_with_token()
    r = requests.post(API_ADDRESS + 'label', headers=headers, json=label)
    if r.status_code != 200:
        return {'error': 'Unauthorized'}, 401
    else: 
        flash(f"Pomyślnie dodano paczkę")
        return redirect(url_for("sender_dashboard"))


@app.route("/package/delete/<id>")
def delete_package(id):
    if "user" not in session:
        flash("Dostęp tylko dla zalogowanych użytkowników!")
        return redirect(url_for("index"))

    headers = generate_header_with_token()
    r = requests.delete(API_ADDRESS + 'label/' + str(id), headers=headers)
    if r.status_code != 200:
        return {'error': 'Unauthorized'}, 401
    else: 
        return redirect(url_for("sender_dashboard"))

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, ssl_context='adhoc')
    app.run(host="0.0.0.0", port=5000, debug=True)