from flask import Flask, render_template
app = Flask(__name__)
app.debug = False

@app.route('/sender/sign-up')
def signUpUser():
    return render_template("register_form.html")

@app.route('/')
def index():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)