from flask import Flask, render_template, request, make_response, session, redirect, url_for
# from flask_session import Session
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# SESSION_TYPE="filesystem"
# SESSION_COOKIE_SECURE = True
app = Flask(__name__)
# app.config.from_object(__name__)
app.secret_key = getenv('SECRET_KEY')

# ses = Session(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sender/register', methods=['GET'])
def register_form():
    return render_template("register_form.html")

@app.route('/sender/register', methods=['POST'])
def register():
    return response

@app.route('/sender/login', methods=['GET'])
def login_form():
    if "user" in session:
        return redirect(url_for("user"))
    return render_template("login_form.html")

@app.route('/sender/login', methods=['POST'])
def login():
    user = request.form["login"]
    session["user"] = user
    session["login_date"] = datetime.now()
    return redirect(url_for("user"))

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)