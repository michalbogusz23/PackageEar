from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from flask_session import Session
from os import getenv
from dotenv import load_dotenv
from datetime import datetime
import sys # for debugging
import db_handler

from redis import Redis
db = Redis(host='redis', port=6379, db=0)

load_dotenv()

SESSION_TYPE="redis"
SESSION_REDIS=db

SESSION_COOKIE_SECURE = True
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

@app.route("/sender/dashboard")
def sender_dashboard():
    if "user" not in session:
        flash("Dostęp tylko dla zalogowanych użytkowników!")
        return redirect(url_for("index"))

    packages = db_handler.get_packages()
    
    return render_template("packages.html", packages=packages)

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

    package = {}
    data = request.form
    fields = ("receiver_name", "box_id", "size")

    if data["size"] not in ["s", "m", "l"]:
        return 'Niewłaściwy rozmiar paczki', 401

    for field in fields:
        package[field] = data[field]

    if db_handler.save_package(package):
        flash(f"Pomyślnie dodano paczkę")
        return redirect(url_for("sender_dashboard"))
    else:
        return "Database not working", 507

@app.route("/package/delete/<id>")
def delete_package(id):
    if "user" not in session:
        flash("Dostęp tylko dla zalogowanych użytkowników!")
        return redirect(url_for("index"))

    db_handler.delete_package_from_db(id)

    return redirect(url_for("sender_dashboard"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, ssl_context='adhoc')
    # app.run(host="0.0.0.0", port=5000, debug=True)